from flask import session, request
from sqlalchemy import desc, asc

from app.models import Oplog
from app import db
from app.models import Promotion_name, Histlatlng, Landhistsup

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
    'price': '一房一价'
}

# order_ad = {
#     '1': "desc",
#     '0': "asc"
# }
#
# hist_col = {
#     '1': Promotion_name.id,
#     '2': Promotion_name.预售许可证号,
#     '3': Promotion_name.项目备案名,
#     '4': Promotion_name.项目推广名,
#     '5': Histlatlng.building_address,
#     '6': Histlatlng.lng,
#     '7': Histlatlng.lat,
#     '8': Landhistsup.plotnum
# }


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


# class HistOrd:
#     @classmethod
#     def histord(cls, ad='1', col='1'):
#         if order_ad[ad] == "desc":
#             return desc(hist_col[col])
#         else:
#             return asc(hist_col[col])
