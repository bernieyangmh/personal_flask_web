# -*-  coding:utf-8 -*-
from flask import Blueprint

main = Blueprint('main', __name__)

#尾部导入避免循环依赖

from . import views, errors
from ..models import Permission

#在模板中检查权限
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
