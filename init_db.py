from app import app
from models import db, Category, User
import os

def init_db():
    if os.path.exists('church.db'):
        os.remove('church.db')

    with app.app_context():
        db.create_all()
        # Initial categories
        categories = [
            Category(name='Diezmos', type='Ingreso'),
            Category(name='Ofrendas', type='Ingreso'),
            Category(name='Misiones', type='Ingreso'),
            Category(name='Salarios', type='Gasto'),
            Category(name='Servicios Públicos', type='Gasto'),
            Category(name='Mantenimiento', type='Gasto'),
            Category(name='Vivienda Ministro', type='Gasto')
        ]
        db.session.bulk_save_objects(categories)

        # Initial admin user
        admin = User(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)

        db.session.commit()
        print("Base de datos inicializada con éxito.")

if __name__ == '__main__':
    init_db()
