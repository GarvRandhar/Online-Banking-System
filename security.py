import secrets
import smtplib
from datetime import datetime, timedelta
from functools import wraps
from flask import session, flash, redirect, url_for, request
from models import db, Account
import pyotp
import qrcode
from io import BytesIO
import base64

class SecurityManager:
    """Handles all security-related operations"""
    
    @staticmethod
    def generate_otp():
        """Generate a 6-digit OTP"""
        return ''.join(secrets.choice('0123456789') for _ in range(6))
    
    @staticmethod
    def create_totp_secret():
        """Create TOTP secret for authenticator apps"""
        return pyotp.random_base32()
    
    @staticmethod
    def generate_qr_code(account_number, totp_secret):
        """Generate QR code for authenticator setup"""
        totp = pyotp.TOTP(totp_secret)
        uri = totp.provisioning_uri(name=account_number, issuer_name='SecureBank Pro')
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buf = BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        
        return base64.b64encode(buf.getvalue()).decode()
    
    @staticmethod
    def verify_otp(otp_secret, otp_code):
        """Verify OTP code"""
        totp = pyotp.TOTP(otp_secret)
        return totp.verify(otp_code)
    
    @staticmethod
    def record_login_attempt(acno, success=True):
        """Record login attempts for security"""
        from models import LoginAttempt
        attempt = LoginAttempt(
            acno=acno,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', ''),
            success=success,
            timestamp=datetime.now()
        )
        db.session.add(attempt)
        db.session.commit()
    
    @staticmethod
    def check_account_lockout(acno, max_attempts=5, lockout_minutes=30):
        """Check if account is locked due to failed attempts"""
        from models import LoginAttempt
        cutoff_time = datetime.now() - timedelta(minutes=lockout_minutes)
        
        failed_attempts = LoginAttempt.query.filter(
            LoginAttempt.acno == acno,
            LoginAttempt.success == False,
            LoginAttempt.timestamp >= cutoff_time
        ).count()
        
        return failed_attempts >= max_attempts

def require_2fa(f):
    """Decorator to require 2FA verification"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if '2fa_verified' not in session or not session['2fa_verified']:
            flash('Two-factor authentication required.', 'warning')
            return redirect(url_for('verify_2fa'))
        return f(*args, **kwargs)
    return decorated_function