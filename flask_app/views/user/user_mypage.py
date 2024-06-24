from flask_app.database import db
from flask import redirect, render_template, session, request
from flask_app.__init__ import app
from flask_app.views.user.common.user_common import is_customer_login
from flask_app.models.functions.event import  read_event, read_event_event_category, read_event_event_name,read_event_one


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
    # セッション変数から選択された値を取得し、その後で削除
    selected_number = session.pop('selected_number', None)
    if selected_number is not None:
        # ticket_info.htmlから遷移してきたときのみ実行する操作
        event_id = request.form.get("event_id")
        event = read_event_one(event_id)
        event.event_cumulative = int(event.event_cumulative + selected_number)
        event.event_evaluate_times = int(event.event_evaluate_times + 1)
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
                    'event.event_value':event.event_value
                    }
        mst_event_dict.append(param)
    return render_template("/user/mypage/user_mypage.html", mst_event = mst_event_dict )

@app.route("/user_user_top/event_check", methods=["GET", "POST"])
def event_check():
    event_id = request.form['event_id']
    event_name = request.form['event_name']
    event_category_id = request.form['event_category_id']
    event_date = request.form['event_date']
    event_place = request.form['event_place']
    event_overview = request.form['event_overview']

    return render_template("/user/event/event_app_check.html",                               event_id=event_id,
                               event_name=event_name,
                               event_category_id=event_category_id,
                               event_date=event_date,
                               event_place=event_place,
                               event_overview=event_overview)