from flask import Blueprint, request, jsonify, abort
from models import db, User, Expense, Split

bp = Blueprint('main', __name__)

@bp.route('/user', methods=['POST'])
def create_user():
    data = request.json
    if not data or not all(key in data for key in ('email', 'name', 'mobile')):
        abort(400, description="Missing required fields")
    
    new_user = User(email=data['email'], name=data['name'], mobile=data['mobile'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@bp.route('/expense', methods=['POST'])
def add_expense():
    data = request.json
    if not data or not all(key in data for key in ('amount', 'description', 'split_method', 'user_id', 'splits')):
        abort(400, description="Missing required fields")
    
    if data['split_method'] not in ['equal', 'exact', 'percentage']:
        abort(400, description="Invalid split method")
    
    new_expense = Expense(
        amount=data['amount'],
        description=data['description'],
        split_method=data['split_method'],
        user_id=data['user_id']
    )
    db.session.add(new_expense)
    db.session.commit()

    total_split = 0
    for split in data['splits']:
        if not all(key in split for key in ('user_id', 'amount')):
            abort(400, description="Invalid split data")
        
        new_split = Split(
            expense_id=new_expense.id,
            user_id=split['user_id'],
            amount=split['amount'],
            percentage=split.get('percentage')
        )
        total_split += split['amount']
        db.session.add(new_split)
    
    if abs(total_split - data['amount']) > 0.01:  # Allow for small floating-point discrepancies
        abort(400, description="Split amounts do not sum to total expense amount")
    
    db.session.commit()
    return jsonify({'message': 'Expense added successfully'}), 201

# ... (keep other routes as they are)