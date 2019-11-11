from werkzeug.utils import secure_filename

from . import admin
from flask import render_template, redirect, url_for, flash, session, request, send_from_directory
from app.admin.forms import LoginForm, PnForm, PwdForm, AdminForm, ActForm, HistForm, HistEditForm, LandEditForm, \
    PriceForm
from app.models import Admin, Adminlog, Oplog, Promotion_name, Activity, User, Histworm, Histlatlng, Landhistsup, \
    Landmanual, Landpart1, Landpart2, Landlatlng
from app import db, app
from functools import wraps
import datetime
from app.admin.transform import TransForm
from sqlalchemy import or_
import os
import uuid
import pandas as pd
import sqlalchemy


# 上下文应用处理器;转化为全局变量
@admin.context_processor
def tpl_extra():
    date = dict(
        online_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    return date


# 登录装饰器
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@admin.route("/")
@admin_login_req
def index():
    return render_template("admin/index.html")


# 登录
@admin.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data["account"]).first()
        if not admin.check_pwd(data["pwd"]):
            flash("密码错误!", 'err')
            return redirect(url_for("admin.login"))
        session["admin"] = data["account"]
        session["admin_id"] = admin.id
        adminlog = Adminlog(
            admin_id=admin.id,
            ip=request.remote_addr
        )
        db.session.add(adminlog)
        db.session.commit()
        return redirect(request.args.get("next") or url_for("admin.hist_list", page=1))
    return render_template("admin/login.html", form=form)


@admin.route("/logout/")
@admin_login_req
def logout():
    session.pop("admin", None)
    session.pop("admin_id", None)
    return redirect(url_for("admin.login"))


# 修改密码
@admin.route("/pwd/", methods=["GET", "POST"])
@admin_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=session["admin"]).first()
        from werkzeug.security import generate_password_hash
        admin.pwd = generate_password_hash(data["new_pwd"])
        db.session.add(admin)
        db.session.commit()
        flash("修改密码成功,请重新登录!", "ok")
        return redirect(url_for("admin.logout"))
    return render_template("admin/pwd.html", form=form)


# 添加推广名
@admin.route("/pn/add/", methods=["GET", "POST"])
@admin_login_req
def pn_add():
    form = PnForm()
    if form.validate_on_submit():
        data = form.data
        pn = Promotion_name.query.filter_by(
            预售许可证号=data["presale_license_number"]
        ).count()
        if pn >= 1:
            flash("推广名已存在!", "err")
            return redirect(url_for('admin.pn_add'))
        pn = Promotion_name(
            预售许可证号=data["presale_license_number"],
            项目备案名=data["building_name"],
            项目推广名=data["building_promotion_name"]
        )
        db.session.add(pn)
        db.session.commit()
        flash("添加推广名成功!", "ok")

        TransForm.oplog_add(o_type='add', type='pn', da_attr=data["presale_license_number"])
        # oplog = Oplog(
        #     admin_id=session["admin_id"],
        #     ip=request.remote_addr,
        #     reason="添加推广名%s" % data["presale_license_number"]
        # )
        # db.session.add(oplog)
        # db.session.commit()

    return render_template("admin/pn_add.html", form=form)


# 推广名列表
@admin.route("/pn/list/<int:page>/", methods=["GET"])
@admin_login_req
def pn_list(page=None):
    if page is None:
        page = 1
    key = request.args.get("key", "")
    page_data = Promotion_name.query.filter(
        or_(
            Promotion_name.预售许可证号.like('%' + key + '%'),
            Promotion_name.项目备案名.like('%' + key + '%'),
            Promotion_name.项目推广名.like('%' + key + '%')
        )
    ).order_by(
        Promotion_name.id.desc()
    ).paginate(page=page, per_page=20)
    return render_template("admin/pn_list.html", key=key, page_data=page_data)


# 推广名删除
@admin.route("/pn/del/<int:id>/", methods=["GET"])
@admin_login_req
def pn_del(id=None):
    pn = Promotion_name.query.filter_by(id=id).first_or_404()
    db.session.delete(pn)
    db.session.commit()
    flash("删除推广名成功!", "ok")

    TransForm.oplog_add(o_type='del', type='pn', da_attr=pn.预售许可证号)
    # oplog = Oplog(
    #     admin_id=session["admin_id"],
    #     ip=request.remote_addr,
    #     reason="删除推广名%s" % pn.presale_license_number
    # )
    # db.session.add(oplog)
    # db.session.commit()

    return redirect(url_for('admin.pn_list', page=1))


# 推广名编辑;修改
@admin.route("/pn/edit/<int:id>/", methods=["GET", "POST"])
@admin_login_req
def pn_edit(id=None):
    form = PnForm()
    pn = Promotion_name.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        pn_count = Promotion_name.query.filter_by(
            预售许可证号=data["presale_license_number"]
        ).count()
        if pn.预售许可证号 != data["presale_license_number"] and \
                pn_count >= 1:  # 判断和标签是否重复
            flash("推广名已存在!", "err")
            return redirect(url_for('admin.pn_edit', id=id))

        pn.预售许可证号 = data["presale_license_number"]
        pn.项目备案名 = data["building_name"]
        pn.项目推广名 = data["building_promotion_name"]

        db.session.add(pn)
        db.session.commit()
        flash("修改推广名成功!", "ok")

        TransForm.oplog_add(o_type='edit', type='pn', da_attr=data["presale_license_number"])

        # oplog = Oplog(
        #     admin_id=session["admin_id"],
        #     ip=request.remote_addr,
        #     reason="修改推广名%s" % data["presale_license_number"]
        # )
        # db.session.add(oplog)
        # db.session.commit()

        redirect(url_for('admin.pn_edit', id=id))
    return render_template('admin/pn_edit.html', form=form, pn=pn)


# 添加活动
@admin.route("/act/add/", methods=["GET", "POST"])
@admin_login_req
def act_add():
    form = ActForm()
    if form.validate_on_submit():
        data = form.data
        act_count = Activity.query.filter_by(
            活动主题=data["theme"]
        ).count()
        if act_count >= 1:
            flash("活动主题已存在!", "err")
            return redirect(url_for('admin.act_add'))
        act = Activity(
            项目名称=data["building_promotion_name"],
            时间=data["date"],
            活动主办单位=data["organizer"],
            活动主题=data["theme"],
            活动情况=data["situation"],
            活动链接=data["link"]
        )
        db.session.add(act)
        db.session.commit()
        flash("添加活动成功!", "ok")

        TransForm.oplog_add(o_type='add', type='act', da_attr=data["theme"])

    return render_template("admin/act_add.html", form=form)


# 活动列表
@admin.route("/act/list/<int:page>/", methods=["GET"])
@admin_login_req
def act_list(page=None):
    if page is None:
        page = 1
    key = request.args.get("key", "")
    page_data = Activity.query.filter(
        or_(
            Activity.项目名称.like('%' + key + '%'),
            Activity.活动主办单位.like('%' + key + '%'),
            Activity.活动主题.like('%' + key + '%'),
            Activity.活动情况.like('%' + key + '%'),
            Activity.活动链接.like('%' + key + '%')
        )
    ).order_by(
        Activity.id.desc()
    ).paginate(page=page, per_page=20)
    return render_template("admin/act_list.html", key=key, page_data=page_data)


# 活动删除
@admin.route("/act/del/<int:id>/", methods=["GET"])
@admin_login_req
def act_del(id=None):
    act = Activity.query.filter_by(id=id).first_or_404()
    db.session.delete(act)
    db.session.commit()
    flash("删除活动成功!", "ok")

    TransForm.oplog_add(o_type='del', type='act', da_attr=act.活动主题)

    return redirect(url_for('admin.act_list', page=1))


# 活动编辑;修改
@admin.route("/act/edit/<int:id>/", methods=["GET", "POST"])
@admin_login_req
def act_edit(id=None):
    form = ActForm()
    act = Activity.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        act_count = Activity.query.filter_by(
            活动主题=data["theme"]
        ).count()
        if act.活动主题 != data["theme"] and \
                act_count >= 1:
            flash("活动主题已存在!", "err")
            return redirect(url_for('admin.act_edit', id=id))

        act.项目名称 = data["building_promotion_name"]
        act.时间 = data["date"]
        act.活动主办单位 = data["organizer"]
        act.活动主题 = data["theme"]
        act.活动情况 = data["situation"]
        act.活动链接 = data["link"]

        db.session.add(act)
        db.session.commit()
        flash("修改活动成功!", "ok")

        TransForm.oplog_add(o_type='edit', type='act', da_attr=data["theme"])

        redirect(url_for('admin.act_edit', id=id))
    return render_template('admin/act_edit.html', form=form, act=act)


# 管理员操作日志
@admin.route("/oplog/list/<int:page>/", methods=["GET"])
@admin_login_req
def oplog_list(page=None):
    if page is None:
        page = 1
    key = request.args.get("key", "")
    page_data = Oplog.query.join(  # 表有外键就需要关联
        Admin
    ).filter(
        Admin.id == Oplog.admin_id,
        or_(
            Admin.name.like('%' + key + '%'),
            Oplog.reason.like('%' + key + '%'),
            Oplog.ip.like('%' + key + '%')
        )
    ).order_by(
        Oplog.addtime.desc()
    ).paginate(page=page, per_page=20)
    return render_template('admin/oplog_list.html', key=key, page_data=page_data)


# 管理员登录日志
@admin.route("/adminloginlog/list/<int:page>/", methods=["GET"])
@admin_login_req
def adminloginlog_list(page=None):
    if page is None:
        page = 1
    key = request.args.get("key", "")
    page_data = Adminlog.query.join(
        Admin
    ).filter(
        Admin.id == Adminlog.admin_id,
        or_(
            Admin.name.like('%' + key + '%'),
            Adminlog.ip.like('%' + key + '%')
        )
    ).order_by(
        Adminlog.addtime.desc()
    ).paginate(page=page, per_page=20)
    return render_template('admin/adminloginlog_list.html', key=key, page_data=page_data)


# 添加管理员
@admin.route("/admin/add/", methods=["GET", "POST"])
@admin_login_req
def admin_add():
    form = AdminForm()
    from werkzeug.security import generate_password_hash
    if form.validate_on_submit():
        data = form.data
        admin_count = Admin.query.filter_by(
            name=data["name"]
        ).count()
        if admin_count >= 1:
            flash("管理员已存在!", "err")
            return redirect(url_for('admin.admin_add'))
        phone_count = Admin.query.filter_by(
            phone=data["phone"]
        ).count()
        if phone_count >= 1:
            flash("该手机号已注册!", "err")
            return redirect(url_for('admin.admin_add'))

        admin = Admin(
            name=data["name"],
            pwd=generate_password_hash(data["pwd"]),
            # role_id=data["role_id"],
            is_super=1,
            holder=data["holder"],
            phone=data["phone"]
        )
        db.session.add(admin)
        db.session.commit()
        flash("添加管理员成功!", "ok")
    return render_template('admin/admin_add.html', form=form)


# 管理员列表
@admin.route("/admin/list/<int:page>/", methods=["GET"])
@admin_login_req
def admin_list(page=None):
    if page is None:
        page = 1
    key = request.args.get("key", "")
    page_data = Admin.query.filter(
        or_(
            Admin.name.like('%' + key + '%')
        )
    ).order_by(
        Admin.addtime.desc()
    ).paginate(page=page, per_page=20)
    return render_template('admin/admin_list.html', key=key, page_data=page_data)


# 会员列表
@admin.route("/user/list/<int:page>/", methods=["GET"])
@admin_login_req
def user_list(page=None):
    if page is None:
        page = 1
    key = request.args.get("key", "")
    page_data = User.query.filter(
        or_(
            User.nickname.like('%' + key + '%'),
            User.email.like('%' + key + '%')
        )
    ).order_by(
        User.id.desc()
    ).paginate(page=page, per_page=20)
    return render_template('admin/user_list.html', page_data=page_data, key=key)


@admin.route("/user/view/<int:id>/", methods=["GET"])
@admin_login_req
def user_view(id=None):
    user = User.query.get_or_404(int(id))
    return render_template('admin/user_view.html', user=user)


# 删除会员
@admin.route("/user/del/<int:id>/", methods=["GET"])
@admin_login_req
def user_del(id=None):
    user = User.query.get_or_404(int(id))
    db.session.delete(user)
    db.session.commit()
    flash("删除会员成功!", "ok")
    TransForm.oplog_add(o_type='del', type='user', da_attr=user.email)

    return redirect(url_for('admin.user_list', page=1))


# 楼盘列表
@admin.route("/hist/list/<int:page>/", methods=["GET"])
@admin_login_req
def hist_list(page=None):
    if page is None:
        page = 1
    key = request.args.get("key", "")
    page_data = db.session.query(
        Promotion_name,
        Histlatlng,
        Landhistsup
    ).outerjoin(
        Histlatlng,
        Histlatlng.presale_license_number == Promotion_name.预售许可证号
    ).outerjoin(
        Landhistsup,
        Landhistsup.presale_license_number == Promotion_name.预售许可证号
    ).filter(
        or_(
            Promotion_name.预售许可证号.like('%' + key + '%'),
            Promotion_name.项目备案名.like('%' + key + '%'),
            Promotion_name.项目推广名.like('%' + key + '%'),
            Histlatlng.building_address.like('%' + key + '%'),
            Landhistsup.plotnum.like('%' + key + '%')
        )
    ).order_by(
        Promotion_name.id.desc()
    ).paginate(page=page, per_page=20)
    return render_template('admin/hist_list.html', page_data=page_data, key=key)


# 添加楼盘
@admin.route("/hist/add/", methods=["GET", "POST"])
@admin_login_req
def hist_add():
    form = HistForm()
    if form.validate_on_submit():
        data = form.data
        hist_count = Promotion_name.query.filter_by(
            预售许可证号=data["presale_license_number"]
        ).count()
        if hist_count >= 1:
            flash("预售许可证号已存在!", "err")
            return redirect(url_for('admin.hist_add'))

        hist = Promotion_name(
            预售许可证号=data["presale_license_number"],
            项目备案名=data["building_name"],
            项目推广名=data["building_promotion_name"]
        )
        hist_latlng = Histlatlng(
            presale_license_number=data["presale_license_number"],
            building_address=data["building_address"],
            lng=data["lng"],
            lat=data["lat"]
        )
        hist_land = Landhistsup(
            plotnum=data["plotnum"],
            building_promotion_name=data["building_promotion_name"],
            presale_license_number=data["presale_license_number"]
        )
        db.session.add(hist)
        db.session.commit()
        db.session.add(hist_latlng)
        db.session.commit()
        db.session.add(hist_land)
        db.session.commit()
        flash("添加成功!", "ok")

        TransForm.oplog_add(o_type='add', type='pl3', da_attr=data["presale_license_number"])

    return render_template("admin/hist_add.html", form=form)


# 楼盘编辑
@admin.route("/hist/edit/<int:id>/<string:presale_license_number>/", methods=["GET", "POST"])
@admin_login_req
def hist_edit(id=None, presale_license_number=None):
    form = HistEditForm()
    hist = Promotion_name.query.get_or_404(int(id))

    histworm = Histworm.query.filter(
        Histworm.预售许可证号 == presale_license_number
    ).first()

    hist_latlng = Histlatlng.query.filter(
        Histlatlng.presale_license_number == presale_license_number
    ).first()
    hist_latlng_count = Histlatlng.query.filter(
        Histlatlng.presale_license_number == presale_license_number
    ).count()

    hist_land = Landhistsup.query.filter(
        Landhistsup.presale_license_number == presale_license_number
    ).first()
    hist_land_count = Landhistsup.query.filter(
        Landhistsup.presale_license_number == presale_license_number
    ).count()

    if form.validate_on_submit():
        data = form.data
        hist_count = Promotion_name.query.filter_by(
            预售许可证号=data["presale_license_number"]
        ).count()
        if hist.预售许可证号 != data["presale_license_number"] and \
                hist_count >= 1:  # 判断和标签是否重复
            flash("预售许可证号已存在!", "err")
            return redirect(url_for('admin.hist_edit', id=id, presale_license_number=presale_license_number))

        hist.预售许可证号 = form.presale_license_number.data
        hist.项目备案名 = form.building_name.data
        hist.项目推广名 = form.building_promotion_name.data

        if hist_latlng_count >= 1:
            hist_latlng.presale_license_number = form.presale_license_number.data
            hist_latlng.building_address = form.building_address.data
            hist_latlng.lng = form.lng.data
            hist_latlng.lat = form.lat.data
        else:
            hist_latlng = Histlatlng(
                presale_license_number=form.presale_license_number.data,
                building_address=form.building_address.data,
                lng=form.lng.data,
                lat=form.lat.data
            )

        if hist_land_count >= 1:
            hist_land.plotnum = form.plotnum.data
            hist_land.building_promotion_name = form.building_promotion_name.data
            hist_land.presale_license_number = form.presale_license_number.data
        else:
            hist_land = Landhistsup(
                plotnum=form.plotnum.data,
                building_promotion_name=form.building_promotion_name.data,
                presale_license_number=form.presale_license_number.data
            )

        db.session.add(hist)
        db.session.commit()

        db.session.add(hist_latlng)
        db.session.commit()

        db.session.add(hist_land)
        db.session.commit()

        flash("修改成功!", "ok")

        TransForm.oplog_add(o_type='edit', type='pl3', da_attr=form.presale_license_number.data)

        redirect(url_for('admin.hist_edit', id=id, presale_license_number=presale_license_number))
    return render_template('admin/hist_edit.html', form=form, hist=hist, hist_latlng=hist_latlng, hist_land=hist_land,
                           histworm=histworm)


# 删除楼盘
@admin.route("/hist/del/<int:id>/<string:presale_license_number>/", methods=["GET"])
@admin_login_req
def hist_del(id=None, presale_license_number=None):
    hist = Promotion_name.query.get_or_404(int(id))
    db.session.delete(hist)
    db.session.commit()

    hist_latlng = Histlatlng.query.filter(
        Histlatlng.presale_license_number == presale_license_number
    )
    if hist_latlng.count() >= 1:
        db.session.delete(hist_latlng.first())
        db.session.commit()

    hist_land = Landhistsup.query.filter(
        Landhistsup.presale_license_number == presale_license_number
    )
    if hist_land.count() >= 1:
        db.session.delete(hist_land.first())
        db.session.commit()

    flash("删除成功!", "ok")
    TransForm.oplog_add(o_type='del', type='pl3', da_attr=hist.预售许可证号)

    return redirect(url_for('admin.hist_list', page=1))


# 地块列表
@admin.route("/land/list/<int:page>/", methods=["GET"])
@admin_login_req
def land_list(page=None):
    if page is None:
        page = 1
    key = request.args.get("key", "")
    page_data = db.session.query(
        Landmanual,
        Landpart1,
        Landpart2,
        Landlatlng
    ).outerjoin(
        Landpart1,
        Landpart1.地块详情 == Landmanual.地块详情
    ).outerjoin(
        Landpart2,
        Landpart2.地块详情 == Landmanual.地块详情
    ).outerjoin(
        Landlatlng,
        Landlatlng.plotnum == Landpart2.地块编号
    ).group_by(
        Landmanual.地块详情
    ).filter(
        or_(
            Landpart1.标题.like('%' + key + '%'),
            Landpart2.地块编号.like('%' + key + '%'),
            Landmanual.地块详情.like('%' + key + '%'),
            Landlatlng.lng.like('%' + key + '%'),
            Landlatlng.lat.like('%' + key + '%')
        )
    ).paginate(page=page, per_page=20)
    return render_template('admin/land_list.html', page_data=page_data, key=key)


# 地块编辑
@admin.route("/land/edit/<string:land_detail>/<string:plotnum>/", methods=["GET", "POST"])
@admin_login_req
def land_edit(land_detail=None, plotnum=None):
    form = LandEditForm()
    land = Landmanual.query.filter(
        Landmanual.地块详情 == land_detail
    ).first()

    landpart1 = Landpart1.query.filter(
        Landpart1.地块详情 == land_detail
    ).first()

    landpart2 = Landpart2.query.filter(
        Landpart2.地块详情 == land_detail
    ).first()

    land_latlng = Landlatlng.query.filter(
        Landlatlng.plotnum == plotnum
    ).first()
    land_latlng_count = Landlatlng.query.filter(
        Landlatlng.plotnum == plotnum
    ).count()

    if form.validate_on_submit():
        land.地块详情 = form.land_detail.data
        land.总用地面积 = form.total_land_area.data
        land.划拨面积 = form.allocated_area.data
        land.住宅面积 = form.house_area.data
        land.商业面积 = form.commercial_area.data
        land.办公面积 = form.office_area.data
        land.其他面积 = form.other_area.data
        land.建筑密度 = form.building_density.data
        land.建筑高度 = form.building_height.data
        land.绿地率 = form.greening_rate.data
        land.备注 = form.remarks.data

        if land_latlng_count >= 1:
            land_latlng.plotnum = form.plotnum.data
            land_latlng.block_location = form.block_location.data
            land_latlng.lng = form.lng.data
            land_latlng.lat = form.lat.data
        else:
            land_latlng = Landlatlng(
                plotnum=form.plotnum.data,
                block_location=form.block_location.data,
                lng=form.lng.data,
                lat=form.lat.data
            )

        db.session.add(land)
        db.session.commit()

        db.session.add(land_latlng)
        db.session.commit()

        flash("修改成功!", "ok")

        TransForm.oplog_add(o_type='edit', type='ll4', da_attr=form.land_detail.data)

        redirect(url_for('admin.land_edit', land_detail=land_detail, plotnum=plotnum))
    return render_template('admin/land_edit.html', form=form, land=land, land_latlng=land_latlng,
                           landpart1=landpart1, landpart2=landpart2)


# 修改上传文件名
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


# 上传文件
@admin.route("/price/add/", methods=["GET", "POST"])
@admin_login_req
def price_add():
    form = PriceForm()
    if form.validate_on_submit():
        file = secure_filename(form.price_file.data.filename)
        if file == 'xlsx':
            file = 'jiage.xlsx'

        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")

        price_file = change_filename(file)
        form.price_file.data.save(app.config["UP_DIR"] + price_file)

        path = os.path.abspath(app.config["UP_DIR"] + price_file)
        data = pd.DataFrame(pd.read_excel(path))

        engine = sqlalchemy.create_engine(
            'mysql+pymysql://root:Blbj123456@rm-bp16nmlmn159wru4reo.mysql.rds.aliyuncs.com:3306/blbj_crawler?charset=utf8')
        data.to_sql('价格', con=engine, if_exists='append',
                    index=False, index_label=False,
                    dtype={
                        "开发单位": sqlalchemy.types.VARCHAR(255),
                        "预售许可证": sqlalchemy.types.VARCHAR(255),
                        "项目名称": sqlalchemy.types.VARCHAR(255),
                        "幢号": sqlalchemy.types.VARCHAR(255),
                        "室号": sqlalchemy.types.VARCHAR(255),
                        "层高（m）": sqlalchemy.types.VARCHAR(255),
                        "户型": sqlalchemy.types.VARCHAR(255),
                        "建筑面积（㎡）": sqlalchemy.types.DECIMAL(10, 2),
                        "套内建筑面积（㎡）": sqlalchemy.types.DECIMAL(10, 2),
                        "公摊建筑面积（㎡）": sqlalchemy.types.DECIMAL(10, 2),
                        "计价单位": sqlalchemy.types.VARCHAR(255),
                        "毛坯销售单价（元/㎡）": sqlalchemy.types.DECIMAL(11, 2),
                        "毛坯销售房屋总价（元）": sqlalchemy.types.DECIMAL(11, 2),
                        "备注": sqlalchemy.types.VARCHAR(255),
                        "备注2": sqlalchemy.types.VARCHAR(255)
                    })
        engine.dispose()

        flash("添加文件成功!", "ok")

        TransForm.oplog_add(o_type='add', type='price', da_attr=price_file)

    return render_template("admin/price_add.html", form=form)


# 下载文件
@admin.route("/price/dn/")
@admin_login_req
def price_dn():
    path = os.path.abspath(app.config["UP_DIR"])
    return send_from_directory(directory=path, filename="jiage.xlsx",
                               as_attachment=True)
