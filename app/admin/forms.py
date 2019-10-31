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
            "placeholder": "请输入密码！"
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


class PnForm(FlaskForm):
    presale_license_number = StringField(
        label="预售许可证号",
        validators=[
            DataRequired("请输入预售许可证号!")
            # length(min=5, message="请输入大于5个字符")
        ],
        description="预售许可证号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入预售许可证号！"
        }
    )
    building_name = StringField(
        label="项目备案名",
        validators=[
            DataRequired("请输入项目备案名!")
            # length(min=5, message="请输入大于5个字符")
        ],
        description="项目备案名",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入项目备案名！"
        }
    )
    building_promotion_name = StringField(
        label="项目推广名",
        validators=[
            DataRequired("请输入项目推广名!")
            # length(min=5, message="请输入大于5个字符")
        ],
        description="项目推广名",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入项目推广名！"
        }
    )
    submit = SubmitField(
        label="编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )
