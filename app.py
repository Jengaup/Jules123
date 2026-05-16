from flask import Flask, request, redirect, url_for, flash, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, Category, Minister, Transaction, User
from datetime import datetime
from decimal import Decimal
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///church.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret-key-for-now'

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Usuario o contraseña inválida')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()

    total_income = sum(t.amount for t in transactions if t.category.type == 'Ingreso')
    total_expense = sum(t.amount for t in transactions if t.category.type == 'Gasto')
    balance = total_income - total_expense

    return render_template('index.html',
                           transactions=transactions,
                           total_income=total_income,
                           total_expense=total_expense,
                           balance=balance)

@app.route('/transaction/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    if request.method == 'POST':
        date_str = request.form.get('date')
        description = request.form.get('description')
        amount = Decimal(request.form.get('amount'))
        category_id = int(request.form.get('category_id'))
        minister_id = request.form.get('minister_id')

        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        new_transaction = Transaction(
            date=date,
            description=description,
            amount=amount,
            category_id=category_id,
            minister_id=int(minister_id) if minister_id else None
        )

        db.session.add(new_transaction)
        db.session.commit()
        flash('Transacción añadida con éxito')
        return redirect(url_for('index'))

    categories = Category.query.all()
    ministers = Minister.query.all()
    return render_template('transaction_form.html', categories=categories, ministers=ministers)

@app.route('/minister/compensation')
@login_required
def minister_compensation():
    ministers = Minister.query.all()
    return render_template('ministers.html', ministers=ministers)

@app.route('/minister/add', methods=['GET', 'POST'])
@login_required
def add_minister():
    if request.method == 'POST':
        name = request.form.get('name')
        base_salary = Decimal(request.form.get('base_salary'))
        housing_allowance = Decimal(request.form.get('housing_allowance'))

        new_minister = Minister(
            name=name,
            base_salary=base_salary,
            housing_allowance=housing_allowance
        )
        db.session.add(new_minister)
        db.session.commit()
        flash('Ministro añadido con éxito')
        return redirect(url_for('minister_compensation'))

    return render_template('minister_form.html')

if __name__ == '__main__':
    app.run(debug=True)
