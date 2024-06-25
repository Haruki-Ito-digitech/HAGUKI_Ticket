from flask import render_template, flash, request, redirect, session,url_for
from flask_app.__init__ import app
from flask_app.messages import ErrorMessages, InfoMessages
from flask_app.models.functions.staff import read_staff_staff_account
from flask_app.models.functions.customer import create_customer
from flask_app.views.user.common.user_common import is_customer_login



# インフォメーションメッセージクラスのインスタンス作成
infoMessages = InfoMessages()
# エラーメッセージクラスのインスタンス作成
errorMessages = ErrorMessages()

def validate_form(form):
    errors = []
    # 各フィールドが空白でないことを確認
    for field, value in form.items():
        if not value:
            errors.append(flash(f'{field}は必須入力です'))

    return errors

# 新規会員登録
@app.route("/user_signup", methods=["GET", "POST"])
@is_customer_login
def user_signup():
    if request.method == 'POST':
        redirect(url_for('user_signup_check'))
    return render_template("/user/signup/user_signup.html")


# 新規会員登録確認画面
@app.route("/user_signup_check", methods=["GET", "POST"])
@is_customer_login
def user_signup_check():
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


# 新規会員登録完了
@app.route("/user_signup_comp", methods=["GET", "POST"])
@is_customer_login
def user_signup_comp():
    create_customer(request)
    return render_template("/user/signup/user_signup_comp.html")


