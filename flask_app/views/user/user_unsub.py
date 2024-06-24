from flask import render_template, flash, request, redirect, session,url_for
from flask_app.__init__ import app
from flask_app.messages import ErrorMessages, InfoMessages
from flask_app.models.functions.staff import read_staff_staff_account
from flask_app.views.staff.common.staff_common import is_staff_login
from flask_app.models.functions.customer import read_customer_one,delete_customer

# インフォメーションメッセージクラスのインスタンス作成
infoMessages = InfoMessages()
# エラーメッセージクラスのインスタンス作成
errorMessages = ErrorMessages()

#会員退会
@app.route("/user_unsub/delete", methods=["GET", "POST"])
# @is_staff_login
def user_delete():
    customer_id = session["logged_in_customer_id"]
    customer = read_customer_one(customer_id)
    return render_template("/user/mypage/unsub/user_unsub_check.html",customer = customer)


#会員退会完了
@app.route("/user_unsub/cmp", methods=["GET", "POST"])
# @is_staff_login
def user_comp():
    customer_id = session["logged_in_customer_id"]
    delete_customer(customer_id)
    return render_template("/user/mypage/unsub/user_unsub_comp.html")

#会員を取得
def user_info():
    account = session["logged_in_customer_account"]
    mst_customer=read_customer_customer_account(account)
    print (mst_customer)
    return render_template("/user/mypage/user_info.html",mst_customer=mst_customer)