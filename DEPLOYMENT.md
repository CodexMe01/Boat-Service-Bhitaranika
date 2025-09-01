# Deployment Guide

This guide covers deploying the Boating Service application to production.

## Prerequisites

- Python 3.8+ installed on your server
- Domain name (optional but recommended)
- SSL certificate (Let's Encrypt or Cloudflare)
- Google Cloud account (for Google Sheets integration)
- Razorpay account (for payments)

## Option 1: Railway Deployment (Recommended)

### 1. Prepare Your Code

1. Push your code to a Git repository (GitHub, GitLab, etc.)
2. Ensure all files are committed except those in `.gitignore`

### 2. Deploy to Railway

1. Go to [Railway.app](https://railway.app) and create an account
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will automatically detect it's a Python app

### 3. Configure Environment Variables

In Railway dashboard, go to your project → Variables tab and add:

```env
FLASK_ENV=production
SECRET_KEY=your-very-long-random-secret-key
RAZORPAY_KEY_ID=rzp_live_XXXXXXXX
RAZORPAY_KEY_SECRET=your_live_secret
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER="Boat Service <your-email@gmail.com>"
GOOGLE_SHEET_ID=your_sheet_id
ADMIN_USERNAME=owner
ADMIN_PASSWORD=your-secure-password
BASE_URL=https://your-app-name.railway.app
```

### 4. Google Sheets Setup

1. Create a Google Cloud Project
2. Enable Google Sheets API
3. Create a Service Account
4. Download the JSON key file
5. In Railway, add a new variable:
   - Key: `GOOGLE_SERVICE_ACCOUNT`
   - Value: Upload the JSON file content (paste the entire JSON)

### 5. Custom Domain (Optional)

1. In Railway, go to Settings → Domains
2. Add your custom domain
3. Update `BASE_URL` in environment variables
4. Configure DNS records as instructed

## Option 2: VPS Deployment

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx -y

# Create application user
sudo useradd -m -s /bin/bash boatapp
sudo usermod -aG sudo boatapp
```

### 2. Application Setup

```bash
# Switch to application user
sudo su - boatapp

# Clone your repository
git clone https://github.com/yourusername/boating-service.git
cd boating-service

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Create environment file
cp env.example .env
nano .env  # Edit with your values
```

### 3. Gunicorn Setup

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/boatapp.service
```

Add this content:

```ini
[Unit]
Description=Boating Service Gunicorn
After=network.target

[Service]
User=boatapp
Group=boatapp
WorkingDirectory=/home/boatapp/boating-service
Environment="PATH=/home/boatapp/boating-service/venv/bin"
ExecStart=/home/boatapp/boating-service/venv/bin/gunicorn --workers 3 --bind unix:boatapp.sock -m 007 app:app

[Install]
WantedBy=multi-user.target
```

### 4. Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/boatapp
```

Add this configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/boatapp/boating-service/boatapp.sock;
    }

    location /static {
        alias /home/boatapp/boating-service/static;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/boatapp /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### 5. SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### 6. Start Services

```bash
sudo systemctl start boatapp
sudo systemctl enable boatapp
sudo systemctl restart nginx
```

## Option 3: Render Deployment

### 1. Prepare Repository

1. Add a `render.yaml` file to your repository:

```yaml
services:
  - type: web
    name: boating-service
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
```

### 2. Deploy to Render

1. Go to [Render.com](https://render.com)
2. Connect your GitHub repository
3. Create a new Web Service
4. Configure environment variables in the dashboard
5. Deploy

## Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `FLASK_ENV` | Environment mode | Yes |
| `SECRET_KEY` | Flask secret key | Yes |
| `RAZORPAY_KEY_ID` | Razorpay public key | Yes |
| `RAZORPAY_KEY_SECRET` | Razorpay secret key | Yes |
| `MAIL_SERVER` | SMTP server | Yes |
| `MAIL_PORT` | SMTP port | Yes |
| `MAIL_USE_TLS` | Use TLS for email | Yes |
| `MAIL_USERNAME` | Email username | Yes |
| `MAIL_PASSWORD` | Email password/app password | Yes |
| `MAIL_DEFAULT_SENDER` | Default sender email | Yes |
| `GOOGLE_SERVICE_ACCOUNT` | Google service account JSON | Yes |
| `GOOGLE_SHEET_ID` | Google Sheet ID | Yes |
| `ADMIN_USERNAME` | Admin panel username | Yes |
| `ADMIN_PASSWORD` | Admin panel password | Yes |
| `BASE_URL` | Application base URL | Yes |

## Post-Deployment Checklist

- [ ] Test the booking flow end-to-end
- [ ] Verify email notifications are working
- [ ] Check Google Sheets integration
- [ ] Test admin panel access
- [ ] Verify file uploads work
- [ ] Test payment integration (use test mode first)
- [ ] Set up monitoring and logging
- [ ] Configure backups
- [ ] Set up rate limiting
- [ ] Test SSL/HTTPS

## Monitoring and Maintenance

### Logs

```bash
# View application logs
sudo journalctl -u boatapp -f

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Backups

Set up regular backups of:
- Database file (`instance/boating.db`)
- Uploaded files (`uploads/`)
- Generated tickets (`instance/tickets/`)
- Environment variables

### Updates

```bash
# Pull latest code
git pull origin main

# Update dependencies
pip install -r requirements.txt

# Restart service
sudo systemctl restart boatapp
```

## Troubleshooting

### Common Issues

1. **500 Internal Server Error**
   - Check application logs
   - Verify environment variables
   - Check file permissions

2. **Payment Issues**
   - Verify Razorpay keys
   - Check webhook configuration
   - Test with test mode first

3. **Email Not Sending**
   - Verify SMTP settings
   - Check app password for Gmail
   - Test SMTP connection

4. **Google Sheets Error**
   - Verify service account permissions
   - Check sheet sharing settings
   - Validate JSON key format

### Support

For deployment issues, check:
- Application logs
- Server logs
- Environment variable configuration
- Network connectivity
- SSL certificate status
