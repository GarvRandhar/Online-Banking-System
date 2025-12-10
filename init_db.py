import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import (
    Account, Amount, Transaction, DebitCard, 
    CurrentAccountApplication, LoanApplication, LoanAccount,
    FixedDeposit, RecurringDeposit, Investment,
    LoginAttempt, TwoFactorAuth
)

def init_database():
    """Initialize database with all tables"""
    with app.app_context():
        print("🔧 Creating database tables...")
        
     
        db.create_all()
        
        print("✅ Database initialized successfully!")
        print("\n📋 Tables created:")
        print("  ✓ Account")
        print("  ✓ Amount")
        print("  ✓ Transaction")
        print("  ✓ DebitCard")
        print("  ✓ CurrentAccountApplication")
        print("  ✓ LoanApplication")
        print("  ✓ LoanAccount")
        print("  ✓ FixedDeposit")
        print("  ✓ RecurringDeposit")
        print("  ✓ Investment")
        print("  ✓ LoginAttempt")
        print("  ✓ TwoFactorAuth")
        print("\n🎉 Database is ready to use!")

if __name__ == '__main__':
    init_database()