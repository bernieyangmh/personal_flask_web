# -*-  coding:utf-8 -*-

import re
import unittest
from flask import url_for
from application import create_app, db
from application.models import WebUser, Role

class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue(b'Stranger' in response.data)

    def test_register_and_login(self):
        # 注册一个用户
        response = self.client.post(url_for('auth.register'), data={
            'email': 'xiaoming@example.com',
            'username': 'xiaoming',
            'password': '123',
            'password2': '123'
        })
        self.assertTrue(response.status_code == 302)

        # 用新用户登录
        response = self.client.post(url_for('auth.login'), data={
            'email': 'xiaoming@example.com',
            'password': '123'
        }, follow_redirects=True)
        self.assertTrue(re.search(b'Hello,\s+john!', response.data))
        self.assertTrue(
            b'您还没确认你的账号' in response.data)

        # 发送一个确认令牌
        user = WebUser.query.filter_by(email='john@example.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get(url_for('auth.confirm', token=token),
                                   follow_redirects=True)
        self.assertTrue(
            b'您已验证账户' in response.data)

        # 注销
        response = self.client.get(url_for('auth.logout'), follow_redirects=True)
        self.assertTrue(b'您已注销' in response.data)
