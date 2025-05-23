from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


# Настройки базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Главная страница с товарами
@app.route('/')
def home():
    return render_template('index.html')

# Страница регистрации
@app.route('/register')
def register():
    return render_template('main.html')

# Обработка формы регистрации
@app.route('/register_user', methods=['POST'])
def register_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))

# Запуск приложения
if __name__ == '__main__':
    db.create_all()  # Создает таблицы в базе данных
    app.run(debug=True)
