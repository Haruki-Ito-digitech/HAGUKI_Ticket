from flask import render_template, flash, request, redirect, session,url_for
from flask_app.__init__ import app
from flask_app.messages import ErrorMessages, InfoMessages
from flask_app.models.functions.staff import read_staff_staff_account
from flask_app.views.staff.common.staff_common import is_staff_login
from flask_app.database import db
from flask_app.models.mst_ticket import Mst_ticket
from flask_app.models.mst_event import Mst_event
from flask_app.models.tbl_reservation import Tbl_reservation
from flask_app.models.functions.reservations import read_reservation_customer_id,param_reservation,delete_reservation

#myチケット一覧画面
@app.route("/my_ticket", methods=["GET", "POST"])
@is_staff_login
def my_ticket():
    logged_in_customer_id = session["logged_in_customer_id"]
    reservation_list = read_reservation_customer_id(logged_in_customer_id)
    reservation_param_list = param_reservation(reservation_list)

    return render_template("user/ticket_manage/my_ticket.html",my_ticket_list = reservation_param_list)

#myチケット詳細画面
@app.route("/ticket_info", methods=["GET", "POST"])
@is_staff_login
def ticket_detail():
    return render_template("user/ticket_manage/ticket_info.html")

#イベントIDとチケットIDを条件に抽出し、myチケットキャンセル画面に表示
@app.route("/ticket_cancel", methods=["GET", "POST"])
@is_staff_login
def read_ticket(event_id,event_category_id):
    ticket_list = Mst_ticket.query.filter(
    Mst_ticket.event_id == event_id).all()
    from flask_app.models.mst_event import Mst_event
    return render_template("user/ticket_manage/cancel/ticket_cancel.html"),ticket_list,event

# チケットを削除し、削除完了画面を表示
@app.route("/ticket_cancel_comp", methods=["GET", "POST"])
@is_staff_login
def delete_ticket(reservation_id):
    delete_reservation(reservation_id)
    return render_template("user/ticket_manage/cancel/ticket_cancel_comp.html")

@app.route("/ticket_cancel_com", methods=["GET", "POST"])
@is_staff_login
def ticket_cancel():
    return render_template("user/ticket_manage/cancel/ticket_cancel.html")

