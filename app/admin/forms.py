from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, SelectMultipleField, \
    DateField, FloatField
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


# 添加推广名
class PnForm(FlaskForm):
    presale_license_number = StringField(
        label="预售许可证号",
        validators=[
            DataRequired("请输入预售许可证号!")
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


# 添加活动
class ActForm(FlaskForm):
    building_promotion_name = StringField(
        label="项目名称",
        validators=[
            DataRequired("请输入项目名称!")
        ],
        description="项目名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入项目名称！"
        }
    )
    date = DateField(
        label="时间",
        validators=[
            DataRequired("请输入时间!")
        ],
        description="时间",
        render_kw={
            "class": "form-control",
            "id": "input_activity_time",
            "placeholder": "请输入时间！"
        }
    )
    organizer = StringField(
        label="活动主办单位",
        validators=[
            DataRequired("请输入活动主办单位!")
        ],
        description="活动主办单位",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入活动主办单位！"
        }
    )
    theme = StringField(
        label="活动主题",
        validators=[
            DataRequired("请输入活动主题!")
        ],
        description="活动主题",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入活动主题！"
        }
    )
    situation = StringField(
        label="活动情况",
        validators=[
            DataRequired("请输入活动情况!")
        ],
        description="活动情况",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入活动情况！"
        }
    )
    link = StringField(
        label="活动链接",
        validators=[
            DataRequired("请输入活动链接!")
        ],
        description="活动链接",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入活动链接！"
        }
    )
    submit = SubmitField(
        label="编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 管理员修改密码
class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label="旧密码",
        validators=[
            DataRequired("请输入旧密码!")
        ],
        description="旧密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入旧密码！"
        }
    )
    new_pwd = PasswordField(
        label="新密码",
        validators=[
            DataRequired("请输入新密码!")
        ],
        description="新密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入新密码！"
        }
    )
    submit = SubmitField(
        label="编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )

    def validate_old_pwd(self, field):
        from flask import session
        pwd = field.data
        name = session["admin"]
        admin = Admin.query.filter_by(
            name=name
        ).first()
        if not admin.check_pwd(pwd):
            raise ValidationError("旧密码错误!")


# 添加管理员
class AdminForm(FlaskForm):
    name = StringField(
        label="管理员名称",
        validators=[
            DataRequired("请输入管理员名称!")
        ],
        description="管理员名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员名称！"
        }
    )
    pwd = PasswordField(
        label="管理员密码",
        validators=[
            DataRequired("请输入管理员密码!")
        ],
        description="管理员密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员密码！"
        }
    )
    repwd = PasswordField(
        label="管理员重复密码",
        validators=[
            DataRequired("请输入管理员重复密码!"),
            EqualTo('pwd', message="两次密码不一致!")
        ],
        description="管理员重复密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员重复密码！"
        }
    )
    # role_id = SelectField(
    #     label="所属角色",
    #     coerce=int,
    #     choices=[(v.id, v.name) for v in role_list],
    #     render_kw={
    #         "class": "form-control"
    #     }
    # )
    submit = SubmitField(
        label="编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 添加活动
class HistForm(FlaskForm):
    presale_license_number = StringField(
        label="预售许可证号",
        validators=[
            DataRequired("请输入预售许可证号!")
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
        ],
        description="项目推广名",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入项目推广名！"
        }
    )
    building_address = StringField(
        label="项目地址",
        validators=[
            DataRequired("请输入项目地址!")
        ],
        description="项目地址",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入项目地址！"
        }
    )
    lng = FloatField(
        label="经度",
        validators=[
            DataRequired("请输入正确的经度!")
        ],
        description="经度",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入经度！"
        }
    )
    lat = FloatField(
        label="纬度",
        validators=[
            DataRequired("请输入正确的纬度!")
        ],
        description="纬度",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入纬度！"
        }
    )
    plotnum = StringField(
        label="地块编号",
        validators=[
            DataRequired("请输入地块编号!")
        ],
        description="地块编号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入地块编号！"
        }
    )
    submit = SubmitField(
        label="编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )