from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_URI = "mysql+pymysql://root:Blbj123456@rm-bp16nmlmn159wru4reo.mysql.rds.aliyuncs.com/movie?charset=utf8"
DB_URI_binds = "mysql+pymysql://{username}:{password}@{host}:{port}/".format(
    username="root",
    password="Blbj123456",
    host="rm-bp16nmlmn159wru4reo.mysql.rds.aliyuncs.com",
    port="3306"
)
SQLAlchemy_binds_local = {
    "ginger": DB_URI_binds + "ginger",
    "blbj_crawler": DB_URI_binds + "blbj_crawler"
}
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config['SQLALCHEMY_BINDS'] = SQLAlchemy_binds_local
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_COMMIT_TEARDOWN"] = True
app.config["SECRET_KEY"] = "887771752dac4713b2c4fdbe8a06d5c2"
app.config["UP_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "files/price_files/")
app.config["LAND_UP_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "files", "land_files")

app.debug = True
db = SQLAlchemy(app)

from app.admin import admin as admin_blueprint

app.register_blueprint(admin_blueprint, url_prefix="/admin")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("admin/404.html"), 404
