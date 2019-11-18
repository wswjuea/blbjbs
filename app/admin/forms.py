from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, SelectMultipleField, \
    DateField, FloatField
from wtforms.validators import DataRequired, ValidationError, EqualTo, length, Regexp

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
        label="确认",
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 添加活动
class ActForm(FlaskForm):
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
        label="确认",
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
        label="确认",
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
    holder = StringField(
        label="持有人姓名",
        validators=[
            DataRequired("请输入持有人姓名!")
        ],
        description="持有人姓名",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入持有人姓名！"
        }
    )
    phone = StringField(
        label="手机号码",
        validators=[
            DataRequired("请输入手机号码!"),
            Regexp("1[3458]\d{9}", message="手机格式不正确!")
        ],
        description="手机号码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入手机号码！"
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
        label="确认",
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 添加楼盘
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
        label="确认",
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 修改楼盘
class HistEditForm(FlaskForm):
    presale_license_number = StringField(
        label="预售许可证号",
        description="预售许可证号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入预售许可证号！",
            "readonly": "true"
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
    remark = StringField(
        label="是否已修改",
        description="是否已修改",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入是否已修改！"
        }
    )
    plotnum = StringField(
        label="地块编号",
        # validators=[
        #     DataRequired("请输入地块编号!")
        # ],
        description="地块编号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入地块编号！"
        }
    )
    completion_date = DateField(
        label="交付时间",
        description="交付时间",
        render_kw={
            "class": "form-control",
            "id": "input_activity_time",
            "placeholder": "请输入交付时间！"
        }
    )
    prop_man_comp = StringField(
        label="物业公司",
        description="物业公司",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入物业公司！"
        }
    )
    floor_area = FloatField(
        label="占地面积",
        description="占地面积",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入占地面积！"
        }
    )
    total_building_volume = StringField(
        label="总建筑体量",
        description="总建筑体量",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入总建筑体量！"
        }
    )
    plot_ratio = StringField(
        label="容积率",
        description="容积率",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入容积率！"
        }
    )
    greening_rate = StringField(
        label="绿地率",
        description="绿地率",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入绿地率！"
        }
    )
    presale_type = StringField(
        label="预售商品房",
        description="预售商品房",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入预售商品房！"
        }
    )
    price_file = FileField(
        label="文件",
        description="文件"
    )
    submit = SubmitField(
        label="确认",
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 修改地块
class LandEditForm(FlaskForm):
    land_detail = StringField(
        label="地块详情",
        description="地块详情",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入地块详情！",
            "readonly": "true"
        }
    )
    plotnum = StringField(
        label="地块编号",
        description="地块编号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入地块编号！",
            "readonly": "true"
        }
    )
    total_land_area = FloatField(
        label="总用地面积",
        # validators=[
        #     DataRequired("请输入总用地面积!")
        # ],
        description="总用地面积",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入总用地面积！"
        }
    )
    allocated_area = FloatField(
        label="划拨面积",
        # validators=[
        #     DataRequired("请输入划拨面积!")
        # ],
        description="划拨面积",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入划拨面积！"
        }
    )
    house_area = FloatField(
        label="住宅面积",
        # validators=[
        #     DataRequired("请输入住宅面积!")
        # ],
        description="住宅面积",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入住宅面积！"
        }
    )
    commercial_area = FloatField(
        label="商业面积",
        # validators=[
        #     DataRequired("请输入商业面积!")
        # ],
        description="商业面积",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入商业面积！"
        }
    )
    office_area = FloatField(
        label="办公面积",
        # validators=[
        #     DataRequired("请输入办公面积!")
        # ],
        description="办公面积",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入办公面积！"
        }
    )
    other_area = FloatField(
        label="其他面积",
        # validators=[
        #     DataRequired("请输入其他面积!")
        # ],
        description="其他面积",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入其他面积！"
        }
    )
    building_density = FloatField(
        label="建筑密度",
        # validators=[
        #     DataRequired("请输入建筑密度!")
        # ],
        description="建筑密度",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入建筑密度！"
        }
    )
    building_height = FloatField(
        label="建筑高度",
        # validators=[
        #     DataRequired("请输入建筑高度!")
        # ],
        description="建筑高度",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入建筑高度！"
        }
    )
    greening_rate = FloatField(
        label="绿地率",
        # validators=[
        #     DataRequired("请输入绿地率!")
        # ],
        description="绿地率",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入绿地率！"
        }
    )
    remarks = StringField(
        label="备注",
        # validators=[
        #     DataRequired("请输入备注!")
        # ],
        description="备注",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入备注！"
        }
    )
    block_location = StringField(
        label="地块位置",
        description="地块位置",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入地块位置！",
            "readonly": "true"
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
    remark = StringField(
        label="是否已修改",
        description="是否已修改",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入是否已修改！"
        }
    )
    submit = SubmitField(
        label="确认",
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 上传到价格表
class PriceForm(FlaskForm):
    price_file = FileField(
        label="文件",
        validators=[
            DataRequired("请上传excel文件!")
        ],
        description="文件"
    )
    submit = SubmitField(
        label="确认",
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 编辑价格
class PriceeditForm(FlaskForm):
    dn = StringField(
        label="开发单位",
        validators=[
            DataRequired("请输入开发单位!")
        ],
        description="开发单位",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入开发单位！"
        }
    )
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
    bn = StringField(
        label="幢号",
        validators=[
            DataRequired("请输入幢号!")
        ],
        description="幢号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入幢号！"
        }
    )
    rn = StringField(
        label="室号",
        validators=[
            DataRequired("请输入室号!")
        ],
        description="室号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入室号！"
        }
    )
    sh = StringField(
        label="层高",
        description="层高",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入层高！"
        }
    )
    apartment = StringField(
        label="户型",
        description="户型",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入户型！"
        }
    )
    area = FloatField(
        label="建筑面积",
        validators=[
            DataRequired("请输入建筑面积!")
        ],
        description="建筑面积",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入建筑面积！"
        }
    )
    biarea = FloatField(
        label="套内建筑面积",
        validators=[
            DataRequired("请输入套内建筑面积!")
        ],
        description="套内建筑面积",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入套内建筑面积！"
        }
    )
    sbarea = FloatField(
        label="公摊建筑面积",
        validators=[
            DataRequired("请输入公摊建筑面积!")
        ],
        description="公摊建筑面积",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入公摊建筑面积！"
        }
    )
    valn = StringField(
        label="计价单位",
        description="计价单位",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入计价单位！"
        }
    )
    room_price = FloatField(
        label="毛坯销售单价",
        validators=[
            DataRequired("请输入毛坯销售单价!")
        ],
        description="毛坯销售单价",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入毛坯销售单价！"
        }
    )
    room_total_price = FloatField(
        label="毛坯销售房屋总价",
        validators=[
            DataRequired("请输入毛坯销售房屋总价!")
        ],
        description="毛坯销售房屋总价",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入毛坯销售房屋总价！"
        }
    )
    remark = StringField(
        label="备注",
        validators=[
            DataRequired("请输入备注!")
        ],
        description="备注",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入备注！"
        }
    )
    remark2 = StringField(
        label="备注2",
        description="备注2",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入备注2！"
        }
    )
    submit = SubmitField(
        label="确认",
        render_kw={
            "class": "btn btn-primary"
        }
    )