from . import admin
from flask import render_template, redirect, url_for


@admin.route("/")
def index():
    return render_template("admin/index.html")


@admin.route("/login/")
def login():
    return render_template("admin/login.html")


@admin.route("/logout/")
def logout():
    return redirect(url_for("admin.login"))


@admin.route("/pwd/")
def pwd():
    return render_template("admin/pwd.html")


# 添加推广名
@admin.route("/pn/add/")
def pn_add():
    return render_template("admin/pn_add.html")


# 推广名列表
@admin.route("/pn/list/")
def pn_list():
    return render_template("admin/pn_list.html")


# 管理员操作日志
@admin.route("/oplog/list/")
def oplog_list():
    return render_template("admin/oplog_list.html")


# 管理员登录日志
@admin.route("/adminloginlog/list/")
def adminloginlog_list():
    return render_template("admin/adminloginlog_list.html")


# 添加管理员
@admin.route("/admin/add/")
def admin_add():
    return render_template('admin/admin_add.html')


# 管理员列表
@admin.route("/admin/list/")
def admin_list():
    return render_template('admin/admin_list.html')
