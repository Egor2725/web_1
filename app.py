
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, LoginManager
from flask_bootstrap import Bootstrap


from flask_migrate import Migrate
from pars_course import show_money
from login import LoginForm
from config import Config
from pars_weather import CityForm, wheather_now, hourly_weather
from pars_films import get_films
from database import db_session




app = Flask(__name__)
login = LoginManager(app)
bootsrap = Bootstrap(app)

app.config.from_object(Config)
# db = SQLAlchemy(app)


money=show_money()      # парсинг валют, передаётся в def course()
movie_list = get_films()
global city_name        #сделал глобальным для передачи между файлами и функциями
city_name = ''




@app.route('/index')
@app.route('/')
def main():                                                  #начальная страница
    user = {'username': 'Egor'}
    return render_template("index.html", user = user)

@app.route('/login', methods=["GET", "POST"])
def log_in():                                                   #страница авторицации
    from models import User#, session
    if current_user.is_authenticated:           #проверка на авторицированного пользователя. но пока не уверен, что работает:D
        print("1111111")       # принты поставил чтоб чекать где код пропускается
        return render_template("/index")
    
    else:
        
        form = LoginForm()
        print("первая остановка")
        if form.validate_on_submit():    #этот блок if почему-то игнорируется                
            print("22222")                 # и при вводе форма пользователя не отправляется, а просто перенапавляется на /login
            from models import User
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or user.check_password(form.password.data)==False:
                print("Прошло")
                flash('Неправильный логин или пароль:c')        #недоконца разобрался ещё с flash, может криво работать
                return redirect('/login')
            login_user(user, remember=form.remember_me.data)
            return redirect('/index')
        else:
            print("остановка")
            return render_template('login.html', form=form, title='Войти')

@app.route('/registration', methods=["GET", "POST"])
def create_account():                                   #регистрация пользователя
    from models import User, create_user
    form = LoginForm()
    if form.validate_on_submit():
        create_user(form.username.data, form.email.data, form.password.data)       #передача данных с формы в БД
        return redirect('/index')
    return render_template('registration.html', form=form, title='Регистрация')    
    

@app.route('/weather/<city_name>', methods=["GET", "POST"])
def weather(city_name):
    form = CityForm()
    
    if form.validate_on_submit():
        city_name = form.city.data
                
        return redirect(f'/weather/{city_name.capitalize()}')   #перенаправление на введенный в форме город

    else:       
        return render_template('page_weather.html',  form=form, wheather_now=wheather_now(city_name), 
                                                            hourly_weather=hourly_weather(city_name), city_name=city_name, title='Погода')
        #передача на страницу формы, погоды сейчас(лев. колонка), почасовой погоды(прав. колонка) и текущего города, поумолчанию это Минск
        #но колонки, пока что, не работают:DD
        


@app.route('/course')
def course():                   #страница с валютами
    return render_template("page_course.html", money=money, title='Курсы валют')

@app.route('/cinema')    
def cinema():
    return render_template("page_films.html", movie_list=movie_list, title='Фильмы')

with app.test_request_context():
    print (url_for("weather", city_name=city_name))


    
    

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()



if __name__ == '__main__':
    app.run(debug=True)
