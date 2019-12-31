from flask import session, request
from sqlalchemy import desc, asc

from app.models import Oplog
from app import db
from app.models import Promotion_name, Histlatlng, Landhistsup, Landpart1, Landpart2, Landmanual, Landlatlng, Landplus

op_type = {
    'add': '添加',
    'edit': '修改',
    'del': '删除'
}
tb_type = {
    'pn': '推广名',
    'act': '活动',
    'user': '会员',
    'pl3': '推广名&hist_latlng&land_histsup',
    'll4': '地块一层&二层&手工&land_latlng',
    'price': '一房一价',
    'landp': 'land_plus'
}

order_ad = {
    '1': "desc",
    '0': "asc"
}

hist_col = {
    '1': Promotion_name.id,
    '2': Promotion_name.预售许可证号,
    '3': Promotion_name.项目备案名,
    '4': Promotion_name.项目推广名,
    '5': Histlatlng.building_address,
    '6': Histlatlng.lng,
    '7': Histlatlng.lat,
    '8': Landhistsup.plotnum,
    '9': Histlatlng.remark
}

land_col = {
    '1': Landpart1.标题,
    '2': Landpart2.地块编号,
    '3': Landmanual.地块详情,
    '4': Landmanual.住宅面积,
    '5': Landmanual.商业面积,
    '6': Landlatlng.lng,
    '7': Landlatlng.lat,
    '8': Landlatlng.remark,
    '9': Landmanual.id
}

land_plus_col = {
    '1': Landplus.plotnum,
    '2': Landplus.house_area,
    '3': Landplus.commercial_area,
    '4': Landlatlng.lng,
    '5': Landlatlng.lat,
    '6': Landlatlng.remark
}

land_file_type = {
    '1': "出让公告",
    '2': "出让须知",
    '3': "宗地界址图",
    '4': "宗地规划指标要求",
    '5': "成交确认书",
    '6': "国有建设用地使用权出让合同"
}


class TransForm:
    @classmethod
    def oplog_add(cls, o_type, type, da_attr):
        oplog = Oplog(
            admin_id=session["admin_id"],
            ip=request.remote_addr,
            reason=op_type[o_type] + tb_type[type] + da_attr
        )
        db.session.add(oplog)
        db.session.commit()
        return None


class HistOrd:
    @classmethod
    def histord(cls, ad, col):
        if order_ad[ad] == "desc":
            return desc(hist_col[col])
        else:
            return asc(hist_col[col])


class LandOrd:
    @classmethod
    def landord(cls, ad, col):
        if order_ad[ad] == "desc":
            return desc(land_col[col])
        else:
            return asc(land_col[col])


class LandplusOrd:
    @classmethod
    def landplusord(cls, ad, col):
        if order_ad[ad] == "desc":
            return desc(land_plus_col[col])
        else:
            return asc(land_plus_col[col])


class CheckLandfile:
    @classmethod
    def check_file_type(cls, filename):
        if filename is not None and filename != "":
            file_type = ['jpg', 'doc', 'docx', 'txt', 'pdf', 'PDF', 'png', 'PNG', 'xls', 'rar', 'exe', 'md', 'zip']
            # 获取文件后缀
            ext = filename.split('.')[1]
            # 判断文件是否是允许上传得类型
            if ext in file_type:
                return True
            else:
                pass
        else:
            pass
