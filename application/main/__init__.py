# -*-  coding:utf-8 -*-
from flask import Blueprint

main = Blueprint('main', __name__)

#尾部导入避免循环依赖

from . import views, errors
