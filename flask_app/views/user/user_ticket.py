from flask import render_template, flash, request, redirect, session,url_for
from flask_app.__init__ import app
from flask_app.messages import ErrorMessages, InfoMessages
from flask_app.models.functions.staff import read_staff_staff_account
from flask_app.database import db
from flask_app.models.mst_ticket import Mst_ticket
from flask_app.models.mst_event import Mst_event
from flask_app.models.tbl_reservation import Tbl_reservation
from flask_app.models.functions.reservations import read_reservation_customer_id,param_reservation,delete_reservation,read_reservation_one,reservation_detail
from flask_app.models.functions.event import read_event_one
from flask_app.views.user.common.user_common import is_customer_login


#myチケット一覧画面
@app.route("/my_ticket", methods=["GET", "POST"])
@is_customer_login
def my_ticket():
    logged_in_customer_id = session["logged_in_customer_id"]
    reservation_list = read_reservation_customer_id(logged_in_customer_id)
    reservation_param_list = param_reservation(reservation_list)
    return render_template("user/ticket_manage/my_ticket.html",my_ticket_list = reservation_param_list)


#myチケット詳細画面
@app.route("/ticket_info/", methods=["GET", "POST"])
@is_customer_login
def ticket_detail():
    reservation_id = request.form.get("reservation_id")
    reservation = read_reservation_one(reservation_id)
    my_ticket = reservation_detail(reservation)
    print('########################')
    print(my_ticket)
    print('########################')

    return render_template("user/ticket_manage/ticket_info.html",my_ticket = my_ticket)

@app.route("/ticket_evaluate", methods=["GET", "POST"])
@is_customer_login
def ticket_evaluate():
    #評価の送信機能　table追加 -> 累積評価cumulative_evaluation　評価された回数 evaluation_times
    selected_number = request.form.get('numbers')
    event_id = request.form.get("event_id")
    session["event_id"] = event_id
    session['selected_number'] = selected_number
    return redirect(url_for('user_user_top'))

# チケットを削除し、削除完了画面を表示
@app.route("/ticket_cancel_comp", methods=["GET", "POST"])
@is_customer_login
def delete_ticket():
    reservation_id = request.form.get("reservation_id")
    delete_reservation(reservation_id)
    return render_template("user/ticket_manage/cancel/ticket_cancel_comp.html")

@app.route("/ticket_cancel_com", methods=["GET", "POST"])
@is_customer_login
def ticket_cancel():
    reservation_id = request.form.get("reservation_id")
    reservation = read_reservation_one(reservation_id)
    my_ticket = reservation_detail(reservation)
    return render_template("user/ticket_manage/cancel/ticket_cancel.html",my_ticket = my_ticket)

