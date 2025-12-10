from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    acno = db.Column(db.String(20), unique=True, nullable=False, index=True)
    dob = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    opening_balance = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    points = db.Column(db.Integer, default=0)
    account_type = db.Column(db.String(20), nullable=False, default='SAVINGS')
    two_factor_enabled = db.Column(db.Boolean, default=False)
    two_factor_secret = db.Column(db.String(32), nullable=True)

    def __repr__(self):
        return f"<Account {self.acno} - {self.name}>"


class Amount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acno = db.Column(db.String(20), unique=True, nullable=False, index=True)
    balance = db.Column(db.Float, nullable=False, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Amount {self.acno} - ₹{self.balance}>"


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acno = db.Column(db.String(20), nullable=False, index=True)
    transaction_type = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    balance_after = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    description = db.Column(db.String(255))
    
    def __repr__(self):
        return f"<Transaction {self.acno} - {self.transaction_type} ₹{self.amount}>"


class DebitCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_number = db.Column(db.String(16), unique=True, nullable=False, index=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    expiry_date = db.Column(db.String(7), nullable=False)
    cvv = db.Column(db.String(3), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<DebitCard {self.card_number}>"


class CurrentAccountApplication(db.Model):
    __tablename__ = 'current_account_application'
    
    id = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.String(10), nullable=False)
    business_type = db.Column(db.String(50), nullable=False)
    company_name = db.Column(db.String(150), nullable=False)
    turnover = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.String(10), nullable=False)
    acno = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default='PENDING')
    applied_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<CurrentAccountApplication {self.acno}>'


class LoanApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acno = db.Column(db.String(20), nullable=False, index=True)
    loan_id = db.Column(db.String(20), unique=True, nullable=False)
    loan_type = db.Column(db.String(50), nullable=False)
    loan_amount = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    processing_fee = db.Column(db.Float, default=0)
    tenure_months = db.Column(db.Integer, nullable=False)
    monthly_emi = db.Column(db.Float, nullable=False)
    
    # Personal details
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    nationality = db.Column(db.String(50), default='Indian')
    
    employment_type = db.Column(db.String(50))
    employment_years = db.Column(db.Integer, default=0)
    company_name = db.Column(db.String(200))
    monthly_salary = db.Column(db.Float)
    annual_income = db.Column(db.Float)
    
    business_type = db.Column(db.String(50))
    business_turnover = db.Column(db.Float)
    
    property_value = db.Column(db.Float)
    
    credit_score = db.Column(db.Integer, default=650)
    existing_loans = db.Column(db.Integer, default=0)
    
    status = db.Column(db.String(20), default='UNDER_REVIEW')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)
    rejected_at = db.Column(db.DateTime)
    rejection_reason = db.Column(db.String(500))
    
    def __repr__(self):
        return f"<LoanApplication {self.loan_id} - {self.status}>"


class LoanAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acno = db.Column(db.String(20), nullable=False, index=True)
    loan_id = db.Column(db.String(20), nullable=False, unique=True)
    loan_type = db.Column(db.String(50), nullable=False)
    principal_amount = db.Column(db.Float, nullable=False)
    disbursed_amount = db.Column(db.Float, nullable=False)
    outstanding_balance = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    tenure_months = db.Column(db.Integer, nullable=False)
    monthly_emi = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='ACTIVE')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    next_emi_date = db.Column(db.Date, nullable=False)
    
    def __repr__(self):
        return f"<LoanAccount {self.loan_id}>"


class FixedDeposit(db.Model):
    """Fixed Deposit accounts"""
    __tablename__ = 'fixed_deposit'
    
    id = db.Column(db.Integer, primary_key=True)
    acno = db.Column(db.String(10), db.ForeignKey('account.acno'), nullable=False)
    fd_id = db.Column(db.String(20), unique=True, nullable=False)
    principal_amount = db.Column(db.Integer, nullable=False)
    interest_rate = db.Column(db.Float, default=6.5)
    tenure_days = db.Column(db.Integer, nullable=False)
    maturity_amount = db.Column(db.Float, nullable=False)
    maturity_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='ACTIVE')
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<FixedDeposit {self.fd_id} - ₹{self.principal_amount}>"


class RecurringDeposit(db.Model):
    """Recurring Deposit accounts"""
    __tablename__ = 'recurring_deposit'
    
    id = db.Column(db.Integer, primary_key=True)
    acno = db.Column(db.String(10), db.ForeignKey('account.acno'), nullable=False)
    rd_id = db.Column(db.String(20), unique=True, nullable=False)
    monthly_amount = db.Column(db.Integer, nullable=False)
    interest_rate = db.Column(db.Float, default=6.0)
    tenure_months = db.Column(db.Integer, nullable=False)
    maturity_amount = db.Column(db.Float, nullable=False)
    maturity_date = db.Column(db.DateTime, nullable=False)
    next_payment_date = db.Column(db.DateTime, nullable=False)
    total_paid = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='ACTIVE')
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<RecurringDeposit {self.rd_id}>"


class Investment(db.Model):
    __tablename__ = 'investment'
    
    id = db.Column(db.Integer, primary_key=True)
    acno = db.Column(db.String(10), db.ForeignKey('account.acno'), nullable=False)
    investment_id = db.Column(db.String(20), unique=True, nullable=False)
    investment_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Float, default=0)
    purchase_price = db.Column(db.Float, default=0)
    current_price = db.Column(db.Float, default=0)
    annual_return = db.Column(db.Float, default=8)
    invested_at = db.Column(db.DateTime, default=datetime.now)
    liquidated_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='ACTIVE')
    
    def __repr__(self):
        return f'<Investment {self.investment_id}>'


class LoginAttempt(db.Model):
    """Track login attempts for security"""
    id = db.Column(db.Integer, primary_key=True)
    acno = db.Column(db.String(20), nullable=False, index=True)
    ip_address = db.Column(db.String(45), nullable=False)
    user_agent = db.Column(db.String(500))
    success = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<LoginAttempt {self.acno} - {'Success' if self.success else 'Failed'}>"


class TwoFactorAuth(db.Model):
    """Store 2FA settings for users"""
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    totp_secret = db.Column(db.String(32), nullable=False)
    backup_codes = db.Column(db.String(500), nullable=False)
    enabled = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<TwoFactorAuth Account {self.account_id}>"


class CreditCard(db.Model):
    __tablename__ = 'credit_card'
    
    id = db.Column(db.Integer, primary_key=True)
    acno = db.Column(db.String(10), db.ForeignKey('account.acno'), nullable=False)
    card_number = db.Column(db.String(16), unique=True, nullable=False)
    card_type = db.Column(db.String(20), nullable=False)
    expiry_date = db.Column(db.String(7), nullable=False)
    cvv = db.Column(db.String(3), nullable=False)
    credit_limit = db.Column(db.Integer, nullable=False)
    available_credit = db.Column(db.Integer, nullable=False)
    current_balance = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='ACTIVE')
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    account = db.relationship('Account', backref='credit_cards')
    
    def __repr__(self):
        return f'<CreditCard {self.card_number[-4:]}'


class CreditCardTransaction(db.Model):
    __tablename__ = 'credit_card_transaction'
    
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('credit_card.id'), nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    merchant = db.Column(db.String(100), nullable=True)
    transaction_date = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(20), default='COMPLETED')
    description = db.Column(db.String(200), nullable=True)
    
    credit_card = db.relationship('CreditCard', backref='transactions')
    
    def __repr__(self):
        return f'<CreditCardTransaction {self.id}>'