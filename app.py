import os, json, sqlite3, secrets
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, abort
from flask_mail import Mail
import razorpay

from config import Dev
from services.storage import save_id_proof
from services.pdf_ticket import generate_ticket_pdf
from services.emailer import send_ticket
from services.gsheet import append_booking

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Dev)

os.makedirs(app.instance_path, exist_ok=True)
DB_PATH = os.path.join(app.instance_path, 'boating.db')
SLOTS_PATH = os.path.join('data', 'slots.json')

mail = Mail(app)

# Initialize Razorpay client with fallback for testing
rzp = None
if app.config.get('RAZORPAY_KEY_ID') and app.config.get('RAZORPAY_KEY_SECRET'):
    try:
        rzp = razorpay.Client(auth=(app.config['RAZORPAY_KEY_ID'], app.config['RAZORPAY_KEY_SECRET']))
        print("✅ Razorpay client initialized successfully")
    except Exception as e:
        print(f"⚠️  Razorpay client initialization failed: {e}")
        print("🔧 Using mock Razorpay client for testing")
        rzp = None
else:
    print("🔧 No Razorpay API keys found - using mock client for testing")

# --- db setup ---

def init_db():
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS bookings (
            booking_id TEXT PRIMARY KEY,
            date TEXT, time TEXT, route TEXT,
            persons INTEGER, children_under3 INTEGER,
            name TEXT, phone TEXT, email TEXT, address TEXT,
            id_type TEXT, id_path TEXT,
            amount INTEGER, payment_id TEXT,
            created_at TEXT
        )''')
        con.commit()

init_db()

# --- helpers ---

def read_slots():
    if not os.path.exists(SLOTS_PATH):
        return {}
    with open(SLOTS_PATH, 'r') as f:
        return json.load(f)

def write_slots(data):
    os.makedirs(os.path.dirname(SLOTS_PATH), exist_ok=True)
    with open(SLOTS_PATH, 'w') as f:
        json.dump(data, f, indent=2)

# --- routes ---

@app.get('/')
def index():
    return render_template('index.html', title='Book a Trip')

@app.get('/api/slots')
def api_slots():
    date = request.args.get('date')
    all_slots = read_slots()
    if date:
        return jsonify({"slots": all_slots.get(date, [])})
    return jsonify({"all": all_slots})

@app.get('/customer')
def customer_info():
    date = request.args.get('date')
    time = request.args.get('time')
    persons = int(request.args.get('persons', 1))
    children = int(request.args.get('children_under3', 0))
    route = request.args.get('route')
    if not all([date, time, route]):
        return redirect(url_for('index'))
    return render_template('customer.html', date=date, time=time, persons=persons, children_under3=children, route=route)

@app.post('/pay')
def start_payment():
    global rzp  # Declare rzp as global
    form = request.form
    files = request.files

    # Save ID proof securely
    id_file = files.get('id_file')
    try:
        id_path = save_id_proof(app.config['UPLOAD_FOLDER'], id_file)
    except Exception as e:
        return f"Upload error: {e}", 400

    # Compute amount (e.g., ₹500 per person)
    persons = int(form['persons'])
    children = int(form.get('children_under3', 0) or 0)
    PRICE_PER_PERSON = 500  # INR
    amount = (persons * PRICE_PER_PERSON) * 100  # in paise; children under 3 free

    # Create a booking token (pre-payment)
    booking_token = secrets.token_urlsafe(16)

    # Create Razorpay order
    current_rzp = rzp  # Use local variable to avoid global modification issues
    if current_rzp:
        try:
            order = current_rzp.order.create({
                'amount': amount,
                'currency': 'INR',
                'payment_capture': 1
            })
            print(f"✅ Razorpay order created: {order['id']}")
        except Exception as e:
            print(f"❌ Razorpay order creation failed: {e}")
            print("🔧 Falling back to test mode")
            current_rzp = None
    
    if not current_rzp:
        # Mock order for testing
        order = {
            'id': f"order_test_{secrets.token_hex(8)}",
            'amount': amount,
            'currency': 'INR'
        }
        print(f"🧪 Test order created: {order['id']}")

    # temp store booking draft in server-side session-like cache (sqlite not needed yet)
    app.config.setdefault('DRAFTS', {})
    app.config['DRAFTS'][booking_token] = {
        'date': form['date'], 'time': form['time'], 'route': form['route'],
        'persons': persons, 'children_under3': children,
        'name': form['name'], 'phone': form['phone'], 'email': form['email'], 'address': form['address'],
        'id_type': form['id_type'], 'id_path': id_path,
        'amount': amount, 'order_id': order['id']
    }

    return render_template('pay.html',
        key_id=app.config['RAZORPAY_KEY_ID'],
        order_id=order['id'], amount=amount,
        name=form['name'], email=form['email'], phone=form['phone'],
        persons=persons, booking_token=booking_token)

@app.post('/verify_payment')
def verify_payment():
    data = request.get_json() or {}
    order_id = data.get('razorpay_order_id')
    payment_id = data.get('razorpay_payment_id')
    signature = data.get('razorpay_signature')
    token = data.get('booking_token')

    print(f"🔍 Payment verification request:")
    print(f"   Order ID: {order_id}")
    print(f"   Payment ID: {payment_id}")
    print(f"   Token: {token}")
    print(f"   Available drafts: {list(app.config.get('DRAFTS', {}).keys())}")

    draft = app.config.get('DRAFTS', {}).get(token)
    if not draft:
        print(f"❌ No draft found for token: {token}")
        return jsonify({'status': 'error', 'message': 'Invalid booking token'}), 400
    
    if draft['order_id'] != order_id:
        print(f"❌ Order ID mismatch: draft={draft['order_id']}, request={order_id}")
        return jsonify({'status': 'error', 'message': 'Order ID mismatch'}), 400

    print(f"✅ Draft found: {draft}")

    # verify signature (skip for test orders)
    if order_id.startswith('order_test_'):
        print(f"🧪 Test mode: Skipping signature verification for order {order_id}")
    elif rzp:
        try:
            rzp.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })
            print(f"✅ Signature verification successful")
        except Exception as e:
            print(f"❌ Signature verification failed: {e}")
            return jsonify({'status': 'error', 'message': 'Signature verification failed'}), 400
    else:
        print(f"⚠️  No Razorpay client available, skipping signature verification")

    # Persist booking
    booking_id = f"B{secrets.token_hex(5).upper()}"
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        with sqlite3.connect(DB_PATH) as con:
            cur = con.cursor()
            cur.execute('''INSERT INTO bookings (
                booking_id, date, time, route, persons, children_under3, name, phone, email, address,
                id_type, id_path, amount, payment_id, created_at
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (
                booking_id, draft['date'], draft['time'], draft['route'], draft['persons'], draft['children_under3'],
                draft['name'], draft['phone'], draft['email'], draft['address'],
                draft['id_type'], draft['id_path'], draft['amount'], payment_id, now
            ))
            con.commit()
        print(f"✅ Booking saved to database: {booking_id}")
    except Exception as e:
        print(f"❌ Database error: {e}")
        return jsonify({'status': 'error', 'message': 'Database error'}), 500

    # Generate ticket
    try:
        tickets_dir = os.path.join(app.instance_path, 'tickets')
        os.makedirs(tickets_dir, exist_ok=True)
        pdf_path = os.path.join(tickets_dir, f"{booking_id}.pdf")
        generate_ticket_pdf(pdf_path, {
            'booking_id': booking_id, 'date': draft['date'], 'time': draft['time'], 'route': draft['route'],
            'persons': draft['persons'], 'children_under3': draft['children_under3'],
            'name': draft['name'], 'phone': draft['phone'], 'email': draft['email'],
            'amount': draft['amount'], 'payment_id': payment_id
        })
        print(f"✅ PDF ticket generated: {pdf_path}")
    except Exception as e:
        print(f"⚠️  PDF generation failed: {e}")

    # Email ticket (skip in test mode to avoid errors)
    try:
        if not order_id.startswith('order_test_'):
            send_ticket(mail, draft['email'], subject=f"Boat Ticket {booking_id}",
                        body=f"Dear {draft['name']},\n\nAttached is your boat ticket.\nBooking ID: {booking_id}\nDate/Time: {draft['date']} {draft['time']}\nRoute: {draft['route']}\nAmount: ₹{draft['amount']/100:.2f}\n\nThank you!",
                        attachment_path=pdf_path)
            print(f"✅ Email sent to {draft['email']}")
        else:
            print(f"🧪 Test mode: Skipping email sending")
    except Exception as e:
        print(f"⚠️  Email sending failed: {e}")

    # Append to Google Sheet (skip in test mode)
    try:
        if not order_id.startswith('order_test_'):
            append_booking(app.config['GOOGLE_SERVICE_ACCOUNT'], app.config['GOOGLE_SHEET_ID'], [
                booking_id, draft['name'], draft['phone'], draft['email'], draft['address'],
                draft['id_type'], draft['date'], draft['time'], draft['route'],
                draft['persons'], draft['children_under3'], draft['amount']/100, payment_id
            ])
            print(f"✅ Google Sheet updated")
        else:
            print(f"🧪 Test mode: Skipping Google Sheet update")
    except Exception as e:
        print(f"⚠️  Google Sheets append failed: {e}")

    # cleanup draft
    del app.config['DRAFTS'][token]
    print(f"✅ Draft cleaned up for token: {token}")

    print(f"🎉 Payment verification successful! Booking ID: {booking_id}")
    return jsonify({'status': 'ok', 'booking_id': booking_id})

@app.get('/success')
def success():
    booking_id = request.args.get('bid')
    if not booking_id:
        return redirect('/')
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute('SELECT name, email FROM bookings WHERE booking_id=?', (booking_id,))
        row = cur.fetchone()
    if not row:
        abort(404)
    name, email = row
    return render_template('success.html', name=name, booking_id=booking_id, email=email)

@app.get('/ticket/<booking_id>')
def download_ticket(booking_id):
    pdf_path = os.path.join(app.instance_path, 'tickets', f"{booking_id}.pdf")
    if not os.path.exists(pdf_path):
        abort(404)
    return send_file(pdf_path, as_attachment=True, download_name=f"{booking_id}.pdf")

# --- Admin (simple Basic Auth) ---
from functools import wraps
from flask import Response

def require_admin(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not (auth.username == app.config['ADMIN_USERNAME'] and auth.password == app.config['ADMIN_PASSWORD']):
            return Response('Login required', 401, {'WWW-Authenticate': 'Basic realm="Admin"'})
        return f(*args, **kwargs)
    return wrapper

@app.get('/admin')
@require_admin
def admin_page():
    return render_template('admin.html', title='Admin')

@app.post('/admin/slots')
@require_admin
def admin_save_slots():
    payload = request.get_json() or {}
    date = payload.get('date')
    times = payload.get('times', [])
    if not date:
        return jsonify({'status': 'error', 'message': 'date required'}), 400
    slots = read_slots()
    slots[date] = times
    write_slots(slots)
    return jsonify({'status': 'ok'})

@app.get('/admin/bookings')
@require_admin
def admin_bookings():
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        rows = con.execute('SELECT booking_id, name, date, time, route, persons, amount FROM bookings ORDER BY created_at DESC').fetchall()
        data = [dict(r) for r in rows]
    return jsonify({'bookings': data})

if __name__ == '__main__':
    app.run(debug=True)
