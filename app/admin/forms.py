from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, EqualTo, length

from app.models import Admin


class LoginForm(FlaskForm):
    """管理员登录表单"""
    account = StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号!")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号！"
        }
    )

    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码!")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码！",
            "required": "required"
        }
    )

    submit = SubmitField(
        label="登录",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat"
        }
    )

    def validate_account(self, field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            raise ValidationError("账号不存在!")
