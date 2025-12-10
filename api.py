from flask import Blueprint, jsonify, request
from functools import wraps
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from models import db, Account, Amount, Transaction
from werkzeug.security import check_password_hash
from datetime import timedelta

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
jwt = JWTManager()

def api_token_required(f):
    """Decorator for API authentication"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function

@api_bp.route('/auth/login', methods=['POST'])
def api_login():
    """API Login endpoint"""
    data = request.get_json()
    
    if not data or not data.get('acno') or not data.get('password'):
        return jsonify({'error': 'Missing credentials'}), 400
    
    user = Account.query.filter_by(acno=data['acno']).first()
    
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(
            identity=user.acno,
            expires_delta=timedelta(hours=24)
        )
        return jsonify({
            'success': True,
            'access_token': access_token,
            'user': {
                'acno': user.acno,
                'name': user.name,
                'account_type': user.account_type
            }
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@api_bp.route('/account/balance', methods=['GET'])
@api_token_required
def api_get_balance():
    """Get account balance"""
    from flask_jwt_extended import get_jwt_identity
    acno = get_jwt_identity()
    
    amount = Amount.query.filter_by(acno=acno).first()
    if not amount:
        return jsonify({'error': 'Account not found'}), 404
    
    return jsonify({
        'success': True,
        'acno': acno,
        'balance': amount.balance
    }), 200

@api_bp.route('/account/details', methods=['GET'])
@api_token_required
def api_get_account_details():
    """Get account details"""
    from flask_jwt_extended import get_jwt_identity
    acno = get_jwt_identity()
    
    account = Account.query.filter_by(acno=acno).first()
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    
    return jsonify({
        'success': True,
        'account': {
            'acno': account.acno,
            'name': account.name,
            'email': account.email,
            'phone': account.phone,
            'account_type': account.account_type,
            'created_at': account.created_at.isoformat()
        }
    }), 200

@api_bp.route('/transaction/transfer', methods=['POST'])
@api_token_required
def api_transfer():
    """Transfer money between accounts"""
    from flask_jwt_extended import get_jwt_identity
    data = request.get_json()
    from_acno = get_jwt_identity()
    to_acno = data.get('to_acno')
    amount = data.get('amount')
    
    if not to_acno or not amount or amount <= 0:
        return jsonify({'error': 'Invalid transfer details'}), 400
    
    sender = Amount.query.filter_by(acno=from_acno).first()
    receiver = Amount.query.filter_by(acno=to_acno).first()
    
    if not sender or not receiver:
        return jsonify({'error': 'Account not found'}), 404
    
    if sender.balance < amount:
        return jsonify({'error': 'Insufficient balance'}), 400
    
    try:
        sender.balance -= amount
        receiver.balance += amount
        
        txn_send = Transaction(
            acno=from_acno,
            transaction_type='TRANSFER',
            amount=amount,
            balance_after=sender.balance,
            description=f'Transfer to {to_acno}'
        )
        txn_receive = Transaction(
            acno=to_acno,
            transaction_type='RECEIVE',
            amount=amount,
            balance_after=receiver.balance,
            description=f'Transfer from {from_acno}'
        )
        
        db.session.add_all([txn_send, txn_receive])
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Transfer successful',
            'transaction_id': txn_send.id
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/transaction/history', methods=['GET'])
@api_token_required
def api_transaction_history():
    """Get transaction history"""
    from flask_jwt_extended import get_jwt_identity
    acno = get_jwt_identity()
    
    limit = request.args.get('limit', 10, type=int)
    transactions = Transaction.query.filter_by(acno=acno).order_by(
        Transaction.timestamp.desc()
    ).limit(limit).all()
    
    return jsonify({
        'success': True,
        'transactions': [{
            'id': txn.id,
            'type': txn.transaction_type,
            'amount': txn.amount,
            'balance_after': txn.balance_after,
            'timestamp': txn.timestamp.isoformat(),
            'description': txn.description
        } for txn in transactions]
    }), 200

@api_bp.route('/loan/applications', methods=['GET'])
@api_token_required
def api_get_loans():
    """Get loan applications"""
    from flask_jwt_extended import get_jwt_identity
    from models import LoanApplication
    
    acno = get_jwt_identity()
    loans = LoanApplication.query.filter_by(acno=acno).all()
    
    return jsonify({
        'success': True,
        'loans': [{
            'loan_id': loan.loan_id,
            'type': loan.loan_type,
            'amount': loan.loan_amount,
            'interest_rate': loan.interest_rate,
            'status': loan.status,
            'monthly_emi': loan.monthly_emi,
            'created_at': loan.created_at.isoformat()
        } for loan in loans]
    }), 200