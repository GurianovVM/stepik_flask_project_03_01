import datetime
import locale

from flask import render_template, redirect, session
from sqlalchemy.sql.expression import func
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, db
from forms import OrderForm, LoginForm, RegisterForm
from models import Category, Dish, Client, Order


def count_dish_nav():
    # считает количество товаров в session['cart'] и возвращает список с количеством и суммой для меню навигации
    dish_list = []
    dish_session = session.get('dish', [])
    if dish_session is None:
        count = 0
    else:
        count = len(dish_session)
    dish_list.append(count)
    dishes = db.session.query(Dish).all()
    money = 0
    for dish in dishes:
        if str(dish.id) in dish_session:
            money += int(dish.price)
    dish_list.append(money)
    return dish_list


@app.route('/')
def home():
    category = db.session.query(Category).all()
    dish_dict = {}
    for cat in category:
        dish_dict[cat.id] = db.session.query(Dish).filter(Dish.category_id == cat.id).order_by(func.random()).limit(3)
    return render_template('index.html', category=category, dishes=dish_dict, count_cart=count_dish_nav(),
                           flag_login=session.get('login', False))


@app.route('/all/<cat>/')
def all_cat(cat):
    dish_dict = {cat: db.session.query(Dish).filter(Dish.category_id == cat).all()}
    category = db.session.query(Category).get(cat)
    return render_template('all.html', category=category, dishes=dish_dict, count_cart=count_dish_nav(),
                           flag_login=session.get('login', False))

@app.route('/addtocart/<id_dish>/')
def addtocart(id_dish):
    # session['dish'] = []
    cart_list = session.get('dish', [])
    cart_list.append(id_dish)
    session['dish'] = cart_list
    return redirect('/cart/')


@app.route('/cart/', methods=['GET', 'POST'])
def cart():
    form = OrderForm()
    cart_list_id = session.get('dish', [])
    dish_list = []
    for dish_id in cart_list_id:
        dish_list.append(db.session.query(Dish).get(dish_id))
    flag_del = session.get('flag_dish_del', False)
    if flag_del:
        session['flag_dish_del'] = False
    client_data = [session.get('client_name', ''), session.get('client_address', ''),
                   session.get('client_email', ''), session.get('client_phone', '')]
    if form.validate_on_submit():
        if len(session['dish']) == 0:
            return render_template('cart.html', count_cart=count_dish_nav(), form=form, dish_list=dish_list,
                                   flag_del=flag_del, flag_login=session.get('login', False), client_data=client_data,
                                   message='Не выбрано ни одного товара')
        client = db.session.query(Client).filter(Client.email == form.email.data).first()
        if client is not None:
            client_id = client.id
            client.name = form.name.data
            client.address = form.address.data
            client.phone = form.phone.data
            db.session.commit()
        else:
            client_new = Client(name=form.name.data, email=form.email.data, address=form.address.data,
                                phone=form.phone.data)
            db.session.add(client_new)
            db.session.commit()
            client_id = client_new.id
        order = Order(name=form.name.data, email=form.email.data, address=form.address.data, phone=form.phone.data,
                      cash=count_dish_nav()[1], status='Выполняется', client_id=client_id, date=datetime.datetime.now())
        db.session.add(order)
        for i in session['dish']:
            dish = db.session.query(Dish).get(int(i))
            order.dishes.append(dish)
        db.session.commit()
        session['client_id'] = client_id
        session['client_name'] = order.name
        session['client_email'] = order.email
        session['client_address'] = order.address
        session['client_phone'] = order.phone
        if session.get('login', False):
            return redirect('/account/')
        else:
            return redirect('/ordered/')
    return render_template('cart.html', count_cart=count_dish_nav(), form=form, dish_list=dish_list,
                           flag_del=flag_del, flag_login=session.get('login', False), client_data=client_data)


@app.route('/cart/del/<dish_id>')
def cart_del_dish(dish_id):
    cart_list = session.get('dish')
    cart_list.remove(dish_id)
    session['dish'] = cart_list
    session['flag_dish_del'] = True
    return redirect('/cart/')


@app.route('/account/')
def account():
    if session.get('login', False):
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
        client_id = session['client_id']
        order_list = db.session.query(Order).filter(Order.client_id == client_id).all()
        client_order_date = {}
        for order in order_list:
            order_string = str(order.date.strftime('%d') + ' ' + order.date.strftime('%B'))
            client_order_date[order.id] = order_string.title()
        return render_template('account.html', count_cart=count_dish_nav(), order_list=order_list,
                               client_order_date=client_order_date, flag_login=session.get('login', False))
    else:
        return redirect('/')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        client = db.session.query(Client).filter(Client.email == email).first()
        if client is not None:
            try:
                if check_password_hash(client.password, password):
                    session['client_id'] = client.id
                    session['client_name'] = client.name
                    session['client_email'] = client.email
                    session['client_address'] = client.address
                    session['client_phone'] = client.phone
                    session['login'] = True
                    return redirect('/account/')
                else:
                    return render_template('login.html', form=form, message='Неверный пароль')
            except AttributeError:
                return render_template('login.html', form=form, message='Пользователь не зарегестрирован',
                                       registration='Регистрация')
        else:
            return render_template('login.html', form=form, message='Пользователь не зарегестрирован',
                                   registration='Регистрация')
    return render_template('login.html', form=form)


@app.route('/logout/')
def logout():
    session['client_id'] = ''
    session['client_name'] = ''
    session['client_email'] = ''
    session['client_address'] = ''
    session['client_phone'] = ''
    session['dish'] = []
    session['login'] = False
    return redirect('/')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        find_client = db.session.query(Client).filter(Client.email == form.email.data).first()
        if find_client is None:
            password_hash = generate_password_hash(form.password.data)
            client = Client(email=form.email.data, password=password_hash)
            db.session.add(client)
            db.session.commit()
            session['client_id'] = client.id
            session['client_name'] = ''
            session['client_email'] = client.email
            session['client_phone'] = ''
            session['login'] = True
            return redirect('/account/')
        else:
            if find_client.password is None:
                find_client.password = generate_password_hash(form.password.data)
                db.session.commit()
                session['client_id'] = find_client.id
                session['client_name'] = find_client.name
                session['client_email'] = find_client.email
                session['client_phone'] = find_client.phone
                session['login'] = True
                return redirect('/account/')
            else:
                return render_template('register.html', form=form, message='Почта уже занята')
    return render_template('register.html', form=form)


@app.route('/ordered/')
def ordered():
    return render_template('ordered.html', login=session.get('login', False))

