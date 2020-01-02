from datetime import datetime
from app import db


# 推广名
class Promotion_name(db.Model):
    __bind_key__ = "blbj_crawler"
    __tablename__ = "推广名"
    id = db.Column(db.Integer, primary_key=True)
    预售许可证号 = db.Column(db.String(255))
    项目备案名 = db.Column(db.String(255))
    项目推广名 = db.Column(db.String(255))

    def __repr__(self):
        return "<Promotion_name %r>" % self.预售许可证号


# 活动
class Activity(db.Model):
    __bind_key__ = "ginger"
    __tablename__ = "activity"
    id = db.Column(db.Integer, primary_key=True)
    building_promotion_name = db.Column(db.String(11))
    date = db.Column(db.Date)
    organizer = db.Column(db.String(255))
    theme = db.Column(db.String(255))
    situation = db.Column(db.String(255))
    link = db.Column(db.String(255))
    status = db.Column(db.SmallInteger)

    def __repr__(self):
        return "<Activity %r>" % self.id


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    holder = db.Column(db.String(100))
    phone = db.Column(db.String(11), unique=True)
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


# 房管网_销售项目2层_已清洗
class Histworm(db.Model):
    __bind_key__ = "blbj_crawler"
    __tablename__ = "房管网_销售项目2层_已清洗"
    id = db.Column(db.Integer, primary_key=True)
    开发单位 = db.Column(db.CHAR(50))
    预售许可证号 = db.Column(db.CHAR(50))
    发证日期 = db.Column(db.Date)
    所在地区 = db.Column(db.CHAR(20))
    样本区域 = db.Column(db.CHAR(20))
    项目测算面积 = db.Column(db.DECIMAL(10, 2))
    项目名称 = db.Column(db.CHAR(50))
    开盘日期 = db.Column(db.Date)
    售楼电话 = db.Column(db.CHAR(30))
    房源总量 = db.Column(db.SmallInteger)
    交付时间 = db.Column(db.Date)
    物业公司 = db.Column(db.CHAR(100))
    占地面积 = db.Column(db.DECIMAL(15, 3))
    总建筑体量 = db.Column(db.Text)
    容积率 = db.Column(db.Text)
    绿地率 = db.Column(db.Text)
    预售商品房 = db.Column(db.CHAR(50))

    def __repr__(self):
        return "<Histworm %r>" % self.id


# hist_latlng
class Histlatlng(db.Model):
    __bind_key__ = "blbj_crawler"
    __tablename__ = "hist_latlng"
    id = db.Column(db.Integer, primary_key=True)
    presale_license_number = db.Column(db.String(255))
    building_address = db.Column(db.String(255))
    lat = db.Column(db.DECIMAL(9, 6))
    lng = db.Column(db.DECIMAL(9, 6))
    remark = db.Column(db.String(50))

    def __repr__(self):
        return "<Histlatlng %r>" % self.id


# land_histsup
class Landhistsup(db.Model):
    __bind_key__ = "blbj_crawler"
    __tablename__ = "land_histsup"
    id = db.Column(db.Integer, primary_key=True)
    plotnum = db.Column(db.String(255))
    building_promotion_name = db.Column(db.String(255))
    presale_license_number = db.Column(db.String(255))

    def __repr__(self):
        return "<Landhistsup %r>" % self.id


# blbj_土地网手工
class Landmanual(db.Model):
    __bind_key__ = "blbj_crawler"
    __tablename__ = "blbj_土地网手工"
    id = db.Column(db.Integer, primary_key=True)
    地块详情 = db.Column(db.Text, primary_key=True)
    总用地面积 = db.Column(db.DECIMAL(20, 2))
    划拨面积 = db.Column(db.DECIMAL(20, 2))
    住宅面积 = db.Column(db.DECIMAL(20, 2))
    商业面积 = db.Column(db.DECIMAL(20, 2))
    办公面积 = db.Column(db.DECIMAL(20, 2))
    其他面积 = db.Column(db.DECIMAL(20, 2))
    建筑密度 = db.Column(db.DECIMAL(10, 2))
    建筑高度 = db.Column(db.DECIMAL(10, 2))
    绿地率 = db.Column(db.DECIMAL(10, 2))
    备注 = db.Column(db.Text)

    def __repr__(self):
        return "<Landmanual %r>" % self.地块详情


# blbj_土地网一层
class Landpart1(db.Model):
    __bind_key__ = "blbj_crawler"
    __tablename__ = "blbj_土地网一层"
    标题 = db.Column(db.Text)
    地块详情 = db.Column(db.Text, primary_key=True)
    地块名称 = db.Column(db.Text)
    地块位置 = db.Column(db.Text)
    土地用途 = db.Column(db.Text)
    保证金 = db.Column(db.DECIMAL(10, 2))
    结束时间 = db.Column(db.Date)
    终止时间 = db.Column(db.Date)

    def __repr__(self):
        return "<Landpart1 %r>" % self.地块详情


# blbj_土地网二层
class Landpart2(db.Model):
    __bind_key__ = "blbj_crawler"
    __tablename__ = "blbj_土地网二层"
    地块详情 = db.Column(db.Text, primary_key=True)
    地块编号 = db.Column(db.Text)
    拍卖开始时间 = db.Column(db.Date)
    挂牌起始时间 = db.Column(db.Date)
    挂牌截止时间 = db.Column(db.Date)
    保证金到账截止时间 = db.Column(db.Date)
    起始价 = db.Column(db.DECIMAL(15, 2))
    竞得单位 = db.Column(db.Text)
    成交时间 = db.Column(db.Date)
    成交价 = db.Column(db.DECIMAL(15, 2))
    出让面积 = db.Column(db.DECIMAL(10, 2))
    所属行政区 = db.Column(db.Text)
    出让年限 = db.Column(db.Text)
    是否有底价 = db.Column(db.Text)
    最高限价 = db.Column(db.DECIMAL(15, 2))
    最高报价 = db.Column(db.DECIMAL(15, 2))
    最高报价单位 = db.Column(db.Text)
    报名开始时间 = db.Column(db.Date)
    报名截止时间 = db.Column(db.Date)
    竞买人条件 = db.Column(db.Text)
    联系人 = db.Column(db.Text)
    联系人电话 = db.Column(db.Text)

    def __repr__(self):
        return "<Landpart2 %r>" % self.地块详情


# land_latlng
class Landlatlng(db.Model):
    __bind_key__ = "blbj_crawler"
    __tablename__ = "land_latlng"
    plotnum = db.Column(db.String(255), primary_key=True)  # 地块编号
    block_location = db.Column(db.String(255))
    lat = db.Column(db.DECIMAL(9, 6))
    lng = db.Column(db.DECIMAL(9, 6))
    remark = db.Column(db.String(50))

    def __repr__(self):
        return "<Landlatlng %r>" % self.plotnum


# land_plus
class Landplus(db.Model):
    __bind_key__ = "blbj_crawler"
    __tablename__ = "land_plus"
    plotnum = db.Column(db.String(255), primary_key=True)  # 地块编号
    uuid = db.Column(db.Text)
    title = db.Column(db.String(255))
    order_title = db.Column(db.String(255))
    block_name = db.Column(db.String(255))
    block_location = db.Column(db.String(255))
    land_usage = db.Column(db.String(255))
    auction_start_date = db.Column(db.Date)
    listing_start_date = db.Column(db.Date)
    listing_deadline = db.Column(db.Date)
    margin_deadline = db.Column(db.Date)
    price = db.Column(db.DECIMAL(15, 2))
    bond = db.Column(db.DECIMAL(15, 2))
    competitive_unit = db.Column(db.String(255))
    end_date = db.Column(db.Date)
    terminal_date = db.Column(db.Date)
    deal_date = db.Column(db.Date)
    deal_price = db.Column(db.DECIMAL(15, 2))
    plot_ratio_detail = db.Column(db.Text)
    granting_area = db.Column(db.DECIMAL(10, 2))
    region = db.Column(db.String(255))
    age_limit = db.Column(db.String(255))
    floor_pirce = db.Column(db.Text)
    range_bidding_increase = db.Column(db.DECIMAL(15, 2))
    price_ceiling = db.Column(db.DECIMAL(15, 2))
    comple_house_area = db.Column(db.DECIMAL(15, 2))
    match_house_area = db.Column(db.DECIMAL(15, 2))
    highest_quotation = db.Column(db.DECIMAL(15, 2))
    highest_quotation_unit = db.Column(db.String(255))
    register_auction_start_date = db.Column(db.Date)
    register_auction_deadline = db.Column(db.Date)
    bidder_conditions = db.Column(db.Text)
    contacts = db.Column(db.Text)
    contacts_phone = db.Column(db.Text)
    state = db.Column(db.String(255))
    plot_ratio = db.Column(db.DECIMAL(10, 2))
    total_land_area = db.Column(db.DECIMAL(20, 2))
    allocated_area = db.Column(db.DECIMAL(20, 2))
    house_area = db.Column(db.DECIMAL(20, 2))
    commercial_area = db.Column(db.DECIMAL(20, 2))
    office_area = db.Column(db.DECIMAL(20, 2))
    other_area = db.Column(db.DECIMAL(20, 2))
    building_density = db.Column(db.DECIMAL(10, 2))
    building_height = db.Column(db.DECIMAL(10, 2))
    greening_rate = db.Column(db.DECIMAL(10, 2))
    remarks = db.Column(db.Text)
    overall_floorage = db.Column(db.DECIMAL(20, 2))
    comprehensive_floor_price = db.Column(db.DECIMAL(10, 2))
    id = db.Column(db.Integer)
    block_status = db.Column(db.String(255))

    def __repr__(self):
        return "<Landplus %r>" % self.plotnum


# 价格
class Price(db.Model):
    __bind_key__ = "blbj_crawler"
    __tablename__ = "价格"
    id = db.Column(db.Integer, primary_key=True)
    开发单位 = db.Column(db.String(255))
    预售许可证 = db.Column(db.String(255))
    项目名称 = db.Column(db.String(255))
    幢号 = db.Column(db.String(255))
    室号 = db.Column(db.String(255))
    层高 = db.Column(db.String(255))
    户型 = db.Column(db.String(255))
    建筑面积 = db.Column(db.DECIMAL(10, 2))
    套内建筑面积 = db.Column(db.DECIMAL(10, 2))
    公摊建筑面积 = db.Column(db.DECIMAL(10, 2))
    计价单位 = db.Column(db.String(255))
    毛坯销售单价 = db.Column(db.DECIMAL(11, 2))
    毛坯销售房屋总价 = db.Column(db.DECIMAL(11, 2))
    备注 = db.Column(db.String(255))
    备注2 = db.Column(db.String(255))

    def __repr__(self):
        return "<Price %r>" % self.id


# pln_price_file
class Plnpricefile(db.Model):
    __bind_key__ = "blbj_crawler"
    __tablename__ = "pln_price_file"
    id = db.Column(db.Integer, primary_key=True)
    presale_license_number = db.Column(db.String(255))
    price_file = db.Column(db.String(255))

    def __repr__(self):
        return "<Plnpricefile %r>" % self.id


# feedback
class Feedback(db.Model):
    __bind_key__ = "ginger"
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime)
    title = db.Column(db.String(50))
    text = db.Column(db.TEXT)
    username = db.Column(db.String(50))
    phone = db.Column(db.String(50))

    def __repr__(self):
        return "<Feedback %r>" % self.id
