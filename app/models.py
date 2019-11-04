from datetime import datetime
from app import db


# 推广名
class Promotion_name(db.Model):
    __tablename__ = "推广名"
    id = db.Column(db.Integer, primary_key=True)
    预售许可证号 = db.Column(db.String(255))
    项目备案名 = db.Column(db.String(255))
    项目推广名 = db.Column(db.String(255))

    def __repr__(self):
        return "<Promotion_name %r>" % self.预售许可证号


# 活动
class Activity(db.Model):
    __tablename__ = "活动"
    id = db.Column(db.Integer, primary_key=True)
    项目名称 = db.Column(db.String(11))
    时间 = db.Column(db.Date)
    活动主办单位 = db.Column(db.String(255))
    活动主题 = db.Column(db.String(255))
    活动情况 = db.Column(db.String(255))
    活动链接 = db.Column(db.String(255))

    def __repr__(self):
        return "<Activity %r>" % self.id


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    is_super = db.Column(db.SmallInteger)  # 0为超级管理员
    # role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    adminlogs = db.relationship("Adminlog", backref='admin')  # 管理员登录日志外键关系关联
    oplogs = db.relationship("Oplog", backref='admin')  # 管理员操作外键关系关联

    def __repr__(self):
        return "<Admin %r>" % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 管理员登录日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Adminlog %r>" % self.id


# 管理员操作日志
class Oplog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    ip = db.Column(db.String(100))
    reason = db.Column(db.String(600))  # 操作原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Oplog %r>" % self.id


# 用户
class User(db.Model):
    __bind_key__ = "ginger"
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.Integer)
    password = db.Column(db.String(100))
    email = db.Column(db.String(24), unique=True)
    status = db.Column(db.SmallInteger)
    nickname = db.Column(db.String(24))
    auth = db.Column(db.SmallInteger)

    def __repr__(self):
        return "<User %r>" % self.id
