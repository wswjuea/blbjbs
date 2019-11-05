from flask import session, request
from app.models import Oplog
from app import db

op_type = {
    'add': '添加',
    'edit': '修改',
    'del': '删除'
}
tb_type = {
    'pn': '推广名',
    'act': '活动',
    'user': '会员',
    'pl3': '推广名&hist_latlng&land_histsup'
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
