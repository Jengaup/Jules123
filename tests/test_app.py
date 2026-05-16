import unittest
from app import app, db
from models import Category, Transaction, Minister, User
from datetime import date
from decimal import Decimal

class ChurchAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SECRET_KEY'] = 'test-key'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            # Initial categories
            if not Category.query.filter_by(name='Diezmos').first():
                c1 = Category(name='Diezmos', type='Ingreso')
                c2 = Category(name='Salarios', type='Gasto')
                db.session.add_all([c1, c2])

            # Add admin user for all tests
            if not User.query.filter_by(username='admin').first():
                admin = User(username='admin')
                admin.set_password('admin123')
                db.session.add(admin)

            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def login_admin(self):
        return self.app.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)

    def test_index_page(self):
        self.login_admin()
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_transaction(self):
        self.login_admin()
        with app.app_context():
            cat = Category.query.filter_by(name='Diezmos').first()
            response = self.app.post('/transaction/add', data={
                'date': '2023-10-27',
                'description': 'Test Income',
                'amount': '100.00',
                'category_id': str(cat.id),
                'minister_id': ''
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Transacci\xc3\xb3n a\xc3\xb1adida con \xc3\xa9xito', response.data)

            t = Transaction.query.first()
            self.assertEqual(t.amount, Decimal('100.00'))

    def test_financial_summary(self):
        self.login_admin()
        with app.app_context():
            cat_in = Category.query.filter_by(name='Diezmos').first()
            cat_out = Category.query.filter_by(name='Salarios').first()

            t1 = Transaction(date=date(2023, 10, 1), description="In", amount=Decimal('500.00'), category_id=cat_in.id)
            t2 = Transaction(date=date(2023, 10, 2), description="Out", amount=Decimal('200.00'), category_id=cat_out.id)
            db.session.add_all([t1, t2])
            db.session.commit()

            response = self.app.get('/')
            self.assertIn(b'500.00', response.data)
            self.assertIn(b'200.00', response.data)
            self.assertIn(b'300.00', response.data) # Balance

    def test_add_minister(self):
        self.login_admin()
        response = self.app.post('/minister/add', data={
            'name': 'Pastor Test',
            'base_salary': '1500.00',
            'housing_allowance': '500.00'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Ministro a\xc3\xb1adido con \xc3\xa9xito', response.data)

        with app.app_context():
            m = Minister.query.filter_by(name='Pastor Test').first()
            self.assertIsNotNone(m)
            self.assertEqual(m.base_salary, Decimal('1500.00'))
            self.assertEqual(m.housing_allowance, Decimal('500.00'))

if __name__ == '__main__':
    unittest.main()
