from . import admin
from flask import render_template, redirect, url_for, flash, session, request
from app.admin.forms import LoginForm, PnForm
from app.models import Admin, Adminlog, Oplog, Promotion_name
from app import db
from functools import wraps


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


@admin.route("/pwd/")
@admin_login_req
def pwd():
    return render_template("admin/pwd.html")


# 添加推广名
@admin.route("/pn/add/", methods=["GET", "POST"])
@admin_login_req
def pn_add():
    form = PnForm()
    if form.validate_on_submit():
        data = form.data
        pn = Promotion_name.query.filter_by(
            presale_license_number=data["presale_license_number"]
        ).count()
        if pn == 1:
            flash("推广名已存在!", "err")
            return redirect(url_for('admin.pn_add'))
        pn = Promotion_name(
            presale_license_number=data["presale_license_number"],
            building_name=data["building_name"],
            building_promotion_name=data["building_promotion_name"]
        )
        db.session.add(pn)
        db.session.commit()
        flash("添加推广名成功!", "ok")
    return render_template("admin/pn_add.html", form=form)


# 推广名列表
@admin.route("/pn/list/<int:page>/", methods=["GET"])
@admin_login_req
def pn_list(page=None):
    if page is None:
        page = 1
    page_data = Promotion_name.query.order_by(
        Promotion_name.id.desc()
    ).paginate(page=page, per_page=1)
    return render_template("admin/pn_list.html", page_data=page_data)


# 管理员操作日志
@admin.route("/oplog/list/")
@admin_login_req
def oplog_list():
    return render_template("admin/oplog_list.html")


# 管理员登录日志
@admin.route("/adminloginlog/list/")
@admin_login_req
def adminloginlog_list():
    return render_template("admin/adminloginlog_list.html")


# 添加管理员
@admin.route("/admin/add/")
@admin_login_req
def admin_add():
    return render_template('admin/admin_add.html')


# 管理员列表
@admin.route("/admin/list/")
@admin_login_req
def admin_list():
    return render_template('admin/admin_list.html')
