import unittest
from application import create_app, db
from application.models import WebUser


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = WebUser(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = WebUser(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = WebUser(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = WebUser(password='cat')
        u2 = WebUser(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)
