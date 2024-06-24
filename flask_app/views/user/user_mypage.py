from flask_app.database import db
from flask import redirect, render_template, session, request
from flask_app.__init__ import app
from flask_app.views.user.common.user_common import is_customer_login
from flask_app.models.functions.event import  read_event, read_event_event_category, read_event_event_name,read_event_one
from flask_app.models.functions.event_category import event_category_name_judge, read_event_category
from flask_app.models.functions.ticket import read_ticket_event_id, read_ticket_event_id, convert_seat_id
from flask_app.models.functions.reservations import create_reservation
from flask_app.models.functions.customer import read_customer_customer_account

"""
# スタッフメニュー（トップページ）
@app.route("/user_user_top", methods=["GET", "POST"])
@is_customer_login
def user_user_top():
    if session["logged_in_customer"] == True:
        return render_template("/user/user_mypage.html")
    else:
        return redirect("/user/user_login.html")
"""
@app.route("/user_user_top", methods=["GET", "POST"])
def user_user_top():

    mst_event_category = read_event_category()
    # セッション変数から選択された値を取得し、その後で削除
    selected_number = session.pop('selected_number', None)
    event_id = session.pop("event_id",None)

    if selected_number is not None:
        # ticket_info.htmlから遷移してきたときのみ実行する操作
        event = read_event_one(event_id)
        event.event_cumulative = int(event.event_cumulative + selected_number)
        event.event_evaluate_times = int(event.event_evaluate_times) + 1
        event.event_value = round(event.event_cumulative/event.event_evaluate_times, 1)
        db.session.commit()

    mst_event = read_event()
    mst_event_dict = []
    for event in mst_event:
        param = {'isDeletable': True,
                    'event_id': event.event_id,
                    'event_category_id': event.event_category_id,
                    'event_name': event.event_name,
                    'event_date': event.event_date,
                    'event_place': event.event_place,
                    'event_overview': event.event_overview,
                    'event_value':event.event_value
                    }
        mst_event_dict.append(param)
        print(param)
    return render_template("/user/mypage/user_mypage.html", mst_event = mst_event_dict, mst_event_category=mst_event_category )

@app.route("/user_user_top/event_info", methods=["GET", "POST"])
def event_info():
    mst_event_category = read_event_category()
    event_id = request.form['event_id']
    event_name = request.form['event_name']
    event_category_id = request.form['event_category_id']
    event_date = request.form['event_date']
    event_place = request.form['event_place']
    event_overview = request.form['event_overview']
    event_category_name = request.form['event_category_name']
    for event_category in mst_event_category:
        event_category_id = int(event_category_id)
        if event_category_id == event_category.event_category_id:
            event_category_name = event_category.event_category_name
    tickets_data = read_ticket_event_id(event_id)
    tickets = []
    for ticket in tickets_data:
        name = convert_seat_id(ticket.ticket_seat_id)
        param = {
            'id': ticket.ticket_seat_id,
            'name': name,
            'price':ticket.ticket_price
        }
        tickets.append(param)
    print(tickets)
        # param = {'id': ticket_seat_id,
        #     'name': name
        #     }
        # tickets.append(param)
    # print(names)
    return render_template("/user/event/event_info.html",  
                               event_id=event_id,
                               event_name=event_name,
                               event_category_id=event_category_id,
                               event_date=event_date,
                               event_place=event_place,
                               mst_event_category=mst_event_category,
                               event_category_name=event_category_name,
                               tickets=tickets,
                               event_overview=event_overview)

@app.route("/user_user_top/event_app", methods=["GET", "POST"])
def event_app():
    mst_event_category = read_event_category()
    event_id = request.form['event_id']
    event_name = request.form['event_name']
    event_category_id = request.form['event_category_id']
    event_date = request.form['event_date']
    event_place = request.form['event_place']
    event_overview = request.form['event_overview']
    ticket_seat_id = request.form['ticket_seat_id']
    ticket_seat_name = request.form['ticket_seat_name']
    for event_category in mst_event_category:
        event_category_id = int(event_category_id)
        if event_category_id == event_category.event_category_id:
            event_category_name = event_category.event_category_name

    tickets_data = read_ticket_event_id(event_id)
    tickets = []
    for ticket in tickets_data:
        name = convert_seat_id(ticket.ticket_seat_id)
        param = {
            'id': ticket.ticket_seat_id,
            'name': name,
            'price':ticket.ticket_price
        }
        tickets.append(param)
    
    print(ticket_seat_id)

    return render_template("/user/event/event_app.html",
                               event_name=event_name,
                               event_id=event_id,
                               event_category_id=event_category_id,
                               event_date=event_date,
                               event_place=event_place,
                               tickets=tickets,
                               ticket_seat_name=ticket_seat_name,
                               mst_event_category=mst_event_category,
                               event_category_name=event_category_name,
                               ticket_seat_id=ticket_seat_id,
                               event_overview=event_overview)


@app.route("/user_user_top/event_app_input", methods=["GET", "POST"])
def event_app_input():
    mst_event_category = read_event_category()
    event_id = request.form['event_id']
    event_name = request.form['event_name']
    event_category_id = request.form['event_category_id']
    event_date = request.form['event_date']
    event_place = request.form['event_place']
    event_overview = request.form['event_overview']
    ticket_seat_id = request.form['ticket_seat_id']
    ticket_price = request.form['ticket_price']
    ticket_seat_name = request.form['ticket_seat_name']



    for event_category in mst_event_category:
        event_category_id = int(event_category_id)
        if event_category_id == event_category.event_category_id:
            event_category_name = event_category.event_category_name
    return render_template("/user/event/event_app_input.html",
                               event_name=event_name,
                               event_id=event_id,
                               event_category_id=event_category_id,
                               event_category_name=event_category_name,
                               event_date=event_date,
                               event_place=event_place,
                               ticket_price=ticket_price,
                               ticket_seat_name=ticket_seat_name,
                               mst_event_category=mst_event_category,
                               ticket_seat_id=ticket_seat_id,
                               event_overview=event_overview)

@app.route("/user_user_top/event_app_check", methods=["GET", "POST"])
def event_app_check():
    mst_event_category = read_event_category()
    event_id = request.form['event_id']
    event_name = request.form['event_name']
    event_category_id = request.form['event_category_id']
    event_date = request.form['event_date']
    event_place = request.form['event_place']
    event_overview = request.form['event_overview']
    ticket_seat_id = request.form['ticket_seat_id']
    ticket_price = request.form['ticket_price']

    customer_account = request.form['customer_account']
    customer_name = request.form['customer_name']
    customer_zipcode = request.form['customer_zipcode']
    customer_address = request.form['customer_address']
    customer_phone = request.form['customer_phone']
    customer_birth = request.form['customer_birth']
    customer_payment = request.form['customer_payment']
    customer_password = request.form['customer_password']

    for event_category in mst_event_category:
        event_category_id = int(event_category_id)
        if event_category_id == event_category.event_category_id:
            event_category_name = event_category.event_category_name


    ticket_list = read_ticket_event_id(event_id)
    for ticketdata in ticket_list:
        if ticketdata.ticket_seat_id == ticket_seat_id:
            ticket_true = ticketdata.ticket_id
            ticket_accept = ticketdata.ticket_accept


    customer_info = read_customer_customer_account(customer_account)
    # customer_id = customer_info.customer_id
    # print(customer_info)
    customer_id = customer_info[0].customer_id


    return render_template("/user/event/event_app_check.html",
                               event_name=event_name,
                               event_id=event_id,
                               event_category_id=event_category_id,
                               event_category_name=event_category_name,
                               event_date=event_date,
                               event_place=event_place,
                               ticket_price=ticket_price,
                               mst_event_category=mst_event_category,
                               ticket_seat_id=ticket_seat_id,
                               customer_zipcode=customer_zipcode,
                               customer_address=customer_address,
                               customer_phonez=customer_phone,
                               customer_birth=customer_birth,
                               customer_phone=customer_phone,
                               customer_payment=customer_payment,
                               customer_account=customer_account,
                               customer_name=customer_name,
                               customer_password=customer_password,
                               ticket_true=ticket_true,
                               ticket_accept=ticket_accept,
                               customer_id  = customer_id,
                               event_overview=event_overview)

@app.route("/user_user_top/event_app_comp", methods=["GET", "POST"])
def event_app_comp():
    mst_event_category = read_event_category()
    event_id = request.form['event_id']
    event_name = request.form['event_name']
    event_category_id = request.form['event_category_id']
    event_date = request.form['event_date']
    event_place = request.form['event_place']
    event_overview = request.form['event_overview']
    ticket_seat_id = request.form['ticket_seat_id']
    ticket_id = request.form['ticket_id']
    ticket_accept = request.form['ticket_accept']

    customer_account = request.form['customer_account']
    customer_id = request.form['customer_id']
    customer_name = request.form['customer_name']
    customer_zipcode = request.form['customer_zipcode']
    customer_address = request.form['customer_address']
    customer_phone = request.form['customer_phone']
    customer_birth = request.form['customer_birth']
    customer_payment = request.form['customer_payment']
    customer_password = request.form['customer_password']


    for event_category in mst_event_category:
        event_category_id = int(event_category_id)
        if event_category_id == event_category.event_category_id:
            event_category_name = event_category.event_category_name


    # ticket = ticket[0]
    # ticket_accept = ticket.ticket_accept
    # ticket_price = ticket.ticket_price
    create_reservation(request)
    return render_template("/user/event/event_app_comp.html")

