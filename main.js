// Работа корзины
class Cart {
    constructor() {
        this.items = JSON.parse(localStorage.getItem('cart')) || [];
        this.updateCartCounter();
    }

    addItem(productId, quantity = 1) {
        const existingItem = this.items.find(item => item.id === productId);
        
        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            this.items.push({ id: productId, quantity });
        }
        
        this.save();
        this.updateCartCounter();
    }

    removeItem(productId) {
        this.items = this.items.filter(item => item.id !== productId);
        this.save();
        this.updateCartCounter();
    }

    save() {
        localStorage.setItem('cart', JSON.stringify(this.items));
    }

    updateCartCounter() {
        const total = this.items.reduce((sum, item) => sum + item.quantity, 0);
        document.getElementById('cartCounter').textContent = total;
    }

    getItems() {
        return this.items;
    }
}

const cart = new Cart();

// Обработчики событий
document.addEventListener('DOMContentLoaded', () => {
    // Добавление в корзину
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', () => {
            const productId = parseInt(button.dataset.id);
            cart.addItem(productId);
            
            // Анимация добавления
            button.textContent = 'Добавлено!';
            setTimeout(() => {
                button.textContent = 'Добавить в корзину';
            }, 2000);
        });
    });

    // Мобильное меню
    document.getElementById('menuToggle').addEventListener('click', () => {
        document.getElementById('navLinks').classList.toggle('active');
    });
});

// Отправка формы заказа
document.getElementById('checkoutForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const items = cart.getItems().map(item => `Товар ID: ${item.id}, Количество: ${item.quantity}`).join('\n');
    
    formData.append('items', items);
    
    try {
        const response = await fetch('/checkout', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            // Очистка корзины после успешного заказа
            cart.items = [];
            cart.save();
            cart.updateCartCounter();
            
            // Перенаправление на страницу успеха
            window.location.href = '/checkout_success';
        }
    } catch (error) {
        console.error('Ошибка при оформлении заказа:', error);
    }
});