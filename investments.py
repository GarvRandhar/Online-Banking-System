import os
import sys
import logging
import random
import string
from models import db, Account, Amount, Transaction, Investment
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InvestmentManager:
    """Enhanced Investment Management System"""
    
    INVESTMENT_OPTIONS = {
        'GOLD': {'annual_return': 4.5, 'risk': 'LOW', 'min': 1000},
        'BOND': {'annual_return': 6.0, 'risk': 'LOW', 'min': 5000},
        'MUTUAL_FUND': {'annual_return': 8.5, 'risk': 'MEDIUM', 'min': 5000},
        'STOCK': {'annual_return': 12.0, 'risk': 'HIGH', 'min': 10000},
    }
    
    def __init__(self):
        self.investment_types = {
            'MUTUAL_FUND': {'price': 150, 'return': 12},
            'STOCK': {'price': 500, 'return': 15},
            'BOND': {'price': 1000, 'return': 6},
            'COMMODITY': {'price': 300, 'return': 10}
        }
    
    @staticmethod
    def validate_investment(acno, investment_type, amount):
        """Comprehensive validation before investment"""
        errors = []
        
        if investment_type not in InvestmentManager.INVESTMENT_OPTIONS:
            errors.append("Invalid investment type")
            return False, errors
        
        min_amount = InvestmentManager.INVESTMENT_OPTIONS[investment_type]['min']
        if amount < min_amount:
            errors.append(f"Minimum amount for {investment_type} is ₹{min_amount}")
        
        account = Account.query.filter_by(acno=acno).first()
        if not account:
            errors.append("Account not found")
            return False, errors
        
        user_amount = Amount.query.filter_by(acno=acno).first()
        if not user_amount or user_amount.balance < amount:
            errors.append("Insufficient balance")
        
        today_investment = Investment.query.filter(
            Investment.acno == acno,
            Investment.invested_at >= datetime.now().replace(hour=0, minute=0, second=0)
        ).with_entities(db.func.sum(Investment.amount)).scalar() or 0
        
        if today_investment + amount > 500000:  
            errors.append("Daily investment limit exceeded (₹5,00,000)")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def create_investment(acno, investment_type, amount):
        """Create investment with validation"""
        valid, errors = InvestmentManager.validate_investment(acno, investment_type, amount)
        
        if not valid:
            return False, "; ".join(errors)
        
        try:
            user_amount = Amount.query.filter_by(acno=acno).first()
            annual_return = InvestmentManager.INVESTMENT_OPTIONS[investment_type]['annual_return']
            
            investment = Investment(
                acno=acno,
                investment_id='INV' + ''.join(random.choices('0123456789', k=8)),
                investment_type=investment_type,
                quantity=1,
                purchase_price=amount,
                current_price=amount,  
                amount=amount,
                annual_return=annual_return,
                invested_at=datetime.now()
            )
            
            user_amount.balance -= amount
            
            txn = Transaction(
                acno=acno,
                transaction_type='INVESTMENT',
                amount=amount,
                balance_after=user_amount.balance,
                description=f'Investment in {investment_type} - {investment.investment_id}',
                timestamp=datetime.now()
            )
            
            db.session.add(investment)
            db.session.add(txn)
            db.session.commit()
            
            logger.info(f"Investment created: {investment.investment_id} for {acno}")
            return True, f"Investment {investment.investment_id} created successfully"
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating investment: {str(e)}")
            return False, "Database error occurred"
    
    @staticmethod
    def simulate_market_price():
        """Simulate market price changes (run daily)"""
        try:
            active_investments = Investment.query.filter_by(status='ACTIVE').all()
            
            for inv in active_investments:
                change_percent = random.uniform(-0.05, 0.10)
                new_price = inv.current_price * (1 + change_percent)
                
                inv.current_price = new_price
                logger.info(f"Price updated: {inv.investment_id} - ₹{new_price:.2f}")
            
            db.session.commit()
            return True, "Market simulation completed"
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Market simulation error: {str(e)}")
            return False, str(e)
    
    @staticmethod
    def calculate_returns(investment):
        """Calculate detailed returns"""
        days_invested = (datetime.now() - investment.invested_at).days
        
        current_value = investment.quantity * investment.current_price
        
        total_return = current_value - investment.amount
        
        if investment.amount > 0:
            return_percent = (total_return / investment.amount) * 100
        else:
            return_percent = 0
        
        if days_invested > 0:
            annualized_return = (return_percent / days_invested) * 365
        else:
            annualized_return = 0
        
        return {
            'principal': investment.amount,
            'current_value': current_value,
            'total_return': total_return,
            'return_percent': return_percent,
            'annualized_return': annualized_return,
            'days_invested': days_invested,
            'current_price': investment.current_price
        }
    
    @staticmethod
    def get_portfolio_summary(acno):
        """Get complete portfolio summary"""
        investments = Investment.query.filter_by(acno=acno, status='ACTIVE').all()
        
        total_invested = 0
        total_current_value = 0
        total_return = 0
        
        portfolio = []
        
        for inv in investments:
            returns = InvestmentManager.calculate_returns(inv)
            
            total_invested += inv.amount
            total_current_value += returns['current_value']
            total_return += returns['total_return']
            
            portfolio.append({
                'investment': inv,
                'returns': returns
            })
        
        return {
            'total_invested': total_invested,
            'total_current_value': total_current_value,
            'total_return': total_return,
            'total_return_percent': (total_return / total_invested * 100) if total_invested > 0 else 0,
            'investments': portfolio
        }
    
    @staticmethod
    def liquidate_investment(investment_id, acno):
        """Liquidate investment with validation"""
        try:
            investment = Investment.query.filter_by(
                investment_id=investment_id,
                acno=acno,
                status='ACTIVE'
            ).first()
            
            if not investment:
                return False, "Investment not found or already liquidated"
            
            returns = InvestmentManager.calculate_returns(investment)
            current_value = returns['current_value']
            profit_loss = returns['total_return']
            
            user_amount = Amount.query.filter_by(acno=acno).first()
            user_amount.balance += current_value
            
            investment.status = 'LIQUIDATED'
            investment.liquidated_at = datetime.now()
            
            txn = Transaction(
                acno=acno,
                transaction_type='INVESTMENT_LIQUIDATION',
                amount=current_value,
                balance_after=user_amount.balance,
                description=f'Investment liquidation - {investment_id} (P/L: ₹{profit_loss:.2f})',
                timestamp=datetime.now()
            )
            
            db.session.add(txn)
            db.session.commit()
            
            logger.info(f"Investment liquidated: {investment_id} - P/L: ₹{profit_loss:.2f}")
            
            return True, {
                'message': 'Investment liquidated successfully',
                'amount': current_value,
                'profit_loss': profit_loss
            }
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Liquidation error: {str(e)}")
            return False, "Liquidation failed"
    
    @staticmethod
    def get_top_performers(acno, limit=5):
        """Get top performing investments"""
        investments = Investment.query.filter_by(acno=acno, status='ACTIVE').all()
        
        performers = []
        for inv in investments:
            returns = InvestmentManager.calculate_returns(inv)
            performers.append((inv, returns['return_percent']))
        
        performers.sort(key=lambda x: x[1], reverse=True)
        
        return performers[:limit]
    
    def get_current_price(self, investment_type):
        """Get current price of an investment"""
        if investment_type in self.investment_types:
            base_price = self.investment_types[investment_type]['price']
            variation = random.uniform(0.95, 1.05)
            return base_price * variation
        return 1000  
    
    def get_expected_return(self, investment_type):
        """Get expected annual return percentage"""
        if investment_type in self.investment_types:
            return self.investment_types[investment_type]['return']
        return 8  
    
    def get_current_value(self, investment):
        """Calculate current value of an investment"""
        try:
            acno = investment.acno
            investment_type = investment.investment_type
            original_amount = investment.amount
            purchase_price = getattr(investment, 'purchase_price', 100)
            annual_return = getattr(investment, 'annual_return', 8)
            
            invested_at = investment.invested_at
            days_held = (datetime.now() - invested_at).days
            
            appreciation_rate = (annual_return / 100) * (days_held / 365)
            current_value = original_amount * (1 + appreciation_rate)
            
            volatility = random.uniform(0.98, 1.02)
            current_value = current_value * volatility
            
            return current_value
        except Exception:
            return investment.amount
    
    def calculate_profit_loss(self, investment):
        """Calculate profit or loss on an investment"""
        current_value = self.get_current_value(investment)
        profit_loss = current_value - investment.amount
        return profit_loss, current_value
    
    def liquidate_investment(self, investment):
        """Prepare investment for liquidation"""
        current_value = self.get_current_value(investment)
        profit_loss = current_value - investment.amount
        
        return {
            'original_amount': investment.amount,
            'current_value': current_value,
            'profit_loss': profit_loss,
            'return_percentage': (profit_loss / investment.amount * 100) if investment.amount > 0 else 0
        }