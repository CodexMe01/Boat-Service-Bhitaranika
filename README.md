# Boating Service – Production-Ready Starter

A clean, production-focused starter for a boating service website with:

* **Frontend:** HTML, CSS, Vanilla JS (no frameworks)
* **Backend:** Python Flask
* **Payments:** Razorpay Checkout (UPI & Cards)
* **Logs:** Google Sheets append for each successful booking
* **PDF Ticket + Email** after payment
* **Admin Panel** for date/time-slot availability & bookings view

## Features

### Customer Booking Flow
1. **Step 1:** Select trip details (date, time, persons, children under 3, route)
2. **Step 2:** Enter customer information and upload ID proof
3. **Step 3:** Payment via Razorpay (UPI & Cards)
4. **Success:** Download PDF ticket and receive email confirmation

### Admin Features
- Manage available dates and time slots
- View all bookings in a table
- Basic authentication protection

### Technical Features
- Secure file uploads for ID proofs
- PDF ticket generation
- Email notifications with attachments
- Google Sheets integration for booking logs
- SQLite database for booking storage
- Responsive design

## Project Structure

```
boating-service/
├─ app.py                 # Main Flask application
├─ config.py              # Configuration management
├─ requirements.txt       # Python dependencies
├─ env.example           # Environment variables template
├─ instance/
│  └─ boating.db         # SQLite database
├─ data/
│  └─ slots.json         # Admin-managed availability
├─ services/
│  ├─ gsheet.py          # Google Sheets helper
│  ├─ emailer.py         # SMTP helper
│  ├─ pdf_ticket.py      # PDF generation
│  └─ storage.py         # File upload utilities
├─ templates/
│  ├─ base.html          # Base template
│  ├─ index.html         # Step 1: Trip details
│  ├─ customer.html      # Step 2: Customer info
│  ├─ pay.html           # Step 3: Payment
│  ├─ success.html       # Booking confirmation
│  └─ admin.html         # Admin panel
├─ static/
│  ├─ css/
│  │  └─ styles.css      # Main stylesheet
│  └─ js/
│     ├─ main.js         # Global scripts
│     └─ admin.js        # Admin panel scripts
└─ uploads/
   └─ id_proofs/         # Stored ID proof files
```

## Setup Instructions

### 1. Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy the example environment file and configure your settings:

```bash
cp env.example .env
```

Edit `.env` with your actual values:

```env
FLASK_ENV=production
SECRET_KEY=your-strong-secret-key-here

# Razorpay (get from Razorpay dashboard)
RAZORPAY_KEY_ID=rzp_test_XXXXXXXX
RAZORPAY_KEY_SECRET=XXXXXXXXXXXX

# Email Configuration (Gmail example)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER="Boat Service <your-email@gmail.com>"

# Google Sheets Integration
GOOGLE_SERVICE_ACCOUNT=/path/to/service-account.json
GOOGLE_SHEET_ID=your_google_sheet_id

# Admin Authentication
ADMIN_USERNAME=owner
ADMIN_PASSWORD=your-secure-password

# Base URL
BASE_URL=http://127.0.0.1:5000
```

### 3. Google Sheets Setup

1. Create a Google Cloud Project
2. Enable Google Sheets API
3. Create a Service Account and download JSON key
4. Share your Google Sheet with the service account email
5. Update `GOOGLE_SERVICE_ACCOUNT` and `GOOGLE_SHEET_ID` in `.env`

### 4. Razorpay Setup

1. Create a Razorpay account
2. Get your test/live API keys from the dashboard
3. Update `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` in `.env`

### 5. Email Setup (Gmail Example)

1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password
3. Use the App Password in `MAIL_PASSWORD`

### 6. Run the Application

```bash
python app.py
```

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000)

Admin panel: [http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin)

## Usage

### Customer Booking Process

1. **Select Trip Details:** Choose date, time, number of persons, and route
2. **Enter Information:** Provide personal details and upload ID proof
3. **Payment:** Complete payment via Razorpay
4. **Confirmation:** Download ticket and receive email

### Admin Panel

1. **Manage Availability:** Add/update available dates and time slots
2. **View Bookings:** See all bookings in a table format
3. **Access:** Use the credentials set in `ADMIN_USERNAME` and `ADMIN_PASSWORD`

## Security Features

- **File Upload Security:** Secure filename handling and type validation
- **Payment Verification:** Razorpay signature verification
- **Admin Authentication:** Basic auth protection for admin panel
- **Environment Variables:** Sensitive data stored in environment variables
- **SQL Injection Protection:** Parameterized queries

## Production Deployment

### Recommended Stack
- **WSGI Server:** Gunicorn
- **Reverse Proxy:** Nginx
- **SSL:** Let's Encrypt or Cloudflare
- **Hosting:** Railway, Render, or VPS

### Deployment Steps

1. **Set Environment Variables:** Configure all required environment variables
2. **Install Dependencies:** `pip install -r requirements.txt`
3. **Database Setup:** SQLite database will be created automatically
4. **File Permissions:** Ensure proper permissions for uploads and instance folders
5. **SSL Configuration:** Set up HTTPS with proper certificates
6. **Domain Configuration:** Update `BASE_URL` in environment variables

### Security Checklist

- [ ] Change default admin credentials
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS
- [ ] Set up proper file permissions
- [ ] Configure rate limiting
- [ ] Set up monitoring and logging
- [ ] Regular backups of database and files

## Customization

### Pricing
Edit the `PRICE_PER_PERSON` variable in `app.py` (currently set to ₹500)

### Routes
Modify the route options in `templates/index.html`

### Email Templates
Customize email content in the `send_ticket` function in `app.py`

### Styling
Modify `static/css/styles.css` for custom styling

## Troubleshooting

### Common Issues

1. **Google Sheets Error:** Check service account permissions and sheet sharing
2. **Email Not Sending:** Verify SMTP settings and app password
3. **Payment Issues:** Ensure Razorpay keys are correct
4. **File Upload Errors:** Check folder permissions

### Logs
Check Flask application logs for detailed error information.

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please check the troubleshooting section or create an issue in the repository.
