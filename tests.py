import unittest
from app import app, db, Usuario
from datetime import datetime

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_registrar_usuario(self):
        response = self.app.post('/usuarios', json={
            'nombres': 'John',
            'apellidos': 'Doe',
            'fecha_nacimiento': '1990-01-01',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Usuario registrado exitosamente', response.get_json()['message'])

    def test_obtener_usuarios(self):
        with app.app_context():
            usuario = Usuario('John', 'Doe', datetime(1990, 1, 1), 'password123')
            db.session.add(usuario)
            db.session.commit()

        response = self.app.get('/registro')
        self.assertEqual(response.status_code, 200)
        datos = response.get_json()
        self.assertEqual(len(datos), 1)
        self.assertEqual(datos[0]['nombres'], 'John')

    def test_eliminar_usuario(self):
        with app.app_context():
            usuario = Usuario('John', 'Doe', datetime(1990, 1, 1), 'password123')
            db.session.add(usuario)
            db.session.commit()
            user_id = usuario.id

        response = self.app.delete(f'/usuarios/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Usuario eliminado exitosamente', response.get_json()['message'])

if __name__ == '__main__':
    unittest.main()
