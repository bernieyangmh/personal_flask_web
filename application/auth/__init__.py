# -*-  coding:utf-8 -*-
"""
用于用户验证的蓝本
"""

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
