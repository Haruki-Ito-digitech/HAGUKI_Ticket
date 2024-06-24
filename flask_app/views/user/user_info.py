from flask import render_template, flash, request, redirect, session,url_for
from flask_app.__init__ import app
from flask_app.messages import ErrorMessages, InfoMessages
from flask_app.models.functions.staff import read_staff_staff_account
from flask_app.models.functions.customer import read_customer_customer_account,read_customer_one
from flask_app.views.staff.common.staff_common import is_staff_login
 
 
# インフォメーションメッセージクラスのインスタンス作成
infoMessages = InfoMessages()
# エラーメッセージクラスのインスタンス作成
errorMessages = ErrorMessages()
 
#会員情報
@app.route("/user_info", methods=["GET", "POST"])
# @is_staff_login
def user_info():
    account = session["logged_in_customer_id"] 
    mst_customer=read_customer_one(account)
    return render_template("/user/mypage/user_info.html",mst_customer=mst_customer)

#会員情報変更入力
@app.route("/user_info_change", methods=["GET", "POST"])
@is_staff_login
def user_info_change(mode):
    customer_id = request.form['customer_id']
    customer_account = request.form['customer_account']
    customer_password = request.form['customer_password']
    customer_name = request.form['customer_name']
    customer_zipcode = request.form['customer_zipcode']
    customer_address = request.form['customer_address']
    customer_phone = request.form['customer_phone']

    isValidateError = False
    # バリデーション
    if len(customer_name) > 20:
            flash(errorMessages.w07('会員名', '20'))
            isValidateError = True

    if len(customer_password) < 6 or len(customer_password) > 10:
            flash(errorMessages.w08('パスワード', '6', '10'))
            isValidateError = True

    if len(customer_zipcode) != 7:
            flash(errorMessages.w06('郵便番号', '7'))
            isValidateError = True

    if re.fullmatch('[0-9]+', customer_zipcode) == None:
            flash(errorMessages.w10('郵便番号'))
            isValidateError = True

    if len(customer_address) > 50:
            flash(errorMessages.w07('住所', '50'))
            isValidateError = True

    if len(customer_phone) > 11 or len(customer_phone) < 10:
            flash(errorMessages.w08('電話番号', '10', '11'))
            isValidateError = True

    if re.fullmatch('[0-9]+', customer_phone) == None:
            flash(errorMessages.w10('電話番号'))
            isValidateError = True


    
#会員情報変更確認
@app.route("/user_info_check", methods=["GET", "POST"])
@is_staff_login
def user_info_check():
    customer_id = request.form.get('customer_id')
    customer_account = request.form.get('customer_account')
    customer_password = request.form.get('customer_password')
    customer_name = request.form.get('customer_name')
    customer_zipcode = request.form.get('customer_zipcode')
    customer_address = request.form.get('customer_address')
    customer_phone = request.form.get('customer_phone')
    customer_birth = request.form.get('customer_birth')

    isValidateError = False
    form = {
        'メールアドレス': request.form.get('customer_account'),
        'パスワード': request.form.get('customer_password'),
        '氏名': request.form.get('customer_name'),
        '郵便番号': request.form.get('customer_zipcode'),
        '住所': request.form.get('customer_address'),
        '電話番号': request.form.get('customer_phone'),
        '生年月日': request.form.get('customer_birth')
        }
    
    errors = validate_form(form)
    
    #バリデーション実装予定
    # customer_accountのバリデーション
    if not customer_account.isalnum():
        flash('メールアドレスが正しくありません')
        redirect(url_for('user_signup'))

    # customer_passwordのバリデーション
    if not customer_password.isalnum() or len(customer_password) > 10:
        flash('パスワードは英数字10文字以内で入力してください')
        isValidateError = True

    # customer_zipcodeのバリデーション
    if not customer_zipcode.isdigit() or len(customer_zipcode) != 7:
        flash('郵便番号は数字7文字で入力してください')
        isValidateError = True

    # customer_phoneのバリデーション
    if not customer_phone.isdigit():
        flash('電話番号は数字のみで入力してください')
        isValidateError = True

    # 必須入力のバリデーション
    if errors:
        for error in errors:
            print(error)
        isValidateError = True

    if isValidateError:
        # エラーがあれば入力画面に戻る
        return redirect(url_for("user_signup"))
    else:
        # エラーがなければ確認画面に遷移
        return render_template("/user/signup/user_signup_check.html",
                           customer_id = customer_id,
                           customer_account = customer_account,
                           customer_password = customer_password,
                           customer_name = customer_name,
                           customer_zipcode = customer_zipcode,
                           customer_address = customer_address,
                           customer_phone = customer_phone,
                           customer_birth = customer_birth)

    return render_template("/user/mypage/info_change/user_info_check.html")
 
#会員情報変更完了
@app.route("/user_info_comp", methods=["GET", "POST"])
@is_staff_login
def user_info_comp():
    return render_template("/user/mypage/info_change/user_info_comp.html")