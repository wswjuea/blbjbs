from . import admin
from flask import render_template, redirect, url_for, flash, session, request
from app.admin.forms import LoginForm, PnForm, PwdForm, AdminForm
from app.models import Admin, Adminlog, Oplog, Promotion_name
from app import db
from functools import wraps
import datetime
from app.admin.transform import TransForm
from sqlalchemy import or_


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
        return redirect(request.args.get("next") or url_for("admin.index"))
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


# 管理员操作日志
@admin.route("/oplog/list/<int:page>/", methods=["GET"])
@admin_login_req
def oplog_list(page=None):
    if page is None:
        page = 1
    page_data = Oplog.query.join(  # 表有外键就需要关联
        Admin
    ).filter(
        Admin.id == Oplog.admin_id
    ).order_by(
        Oplog.addtime.desc()
    ).paginate(page=page, per_page=20)
    return render_template('admin/oplog_list.html', page_data=page_data)


# 管理员登录日志
@admin.route("/adminloginlog/list/<int:page>/", methods=["GET"])
@admin_login_req
def adminloginlog_list(page=None):
    if page is None:
        page = 1
    page_data = Adminlog.query.join(
        Admin
    ).filter(
        Admin.id == Adminlog.admin_id
    ).order_by(
        Adminlog.addtime.desc()
    ).paginate(page=page, per_page=20)
    return render_template('admin/adminloginlog_list.html', page_data=page_data)


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
        admin = Admin(
            name=data["name"],
            pwd=generate_password_hash(data["pwd"]),
            # role_id=data["role_id"],
            is_super=1
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
    page_data = Admin.query.order_by(
        Admin.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/admin_list.html', page_data=page_data)
