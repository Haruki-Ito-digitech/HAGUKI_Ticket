from flask_app.__init__ import app
from flask import render_template, Flask, session
import flask_app.views.entries
import flask_app.views.staff.common.staff_common
import flask_app.views.staff.staff_top
import flask_app.views.staff.staff_customer
import flask_app.views.staff.staff_login
import flask_app.views.staff.staff_reservation
import flask_app.views.staff.staff_ticket
import flask_app.views.staff.staff_event_category
import flask_app.views.staff.staff_event
import flask_app.views.user.user_login
import flask_app.views.user.user_signup


app.secret_key = 'hoge'

if __name__ == '__main__':
    app.run()

