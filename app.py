from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Конфигурация Telegram бота
TELEGRAM_BOT_TOKEN = 'ВАШ_TELEGRAM_BOT_TOKEN'
TELEGRAM_CHAT_ID = 'ВАШ_CHAT_ID'

# Моковые данные товаров
products = [
    {"id": 1, "name": "Rolex Submariner", "price": 12000, "image": "watch1.webp"},
    {"id": 2, "name": "Rolex Daytona", "price": 15000, "image": "watch2.webp"},
    # ... другие товары
]

@app.route('/')
def index():
    return render_template('index.html', featured_products=products[:4])

@app.route('/catalog')
def catalog():
    return render_template('catalog.html', products=products)

@app.route('/product/<int:product_id>')
def product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return render_template('product.html', product=product)
    return "Товар не найден", 404

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/api/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.json
    # Здесь логика добавления в корзину
    return jsonify(success=True)

@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.form
    # Отправка уведомления в Telegram
    message = f"Новый заказ!\nИмя: {data['name']}\nТелефон: {data['phone']}\nТовары: {data['items']}"
    send_telegram_message(message)
    return render_template('checkout_success.html')

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text
    }
    requests.post(url, data=payload)

if __name__ == '__main__':
    app.run(debug=True)
