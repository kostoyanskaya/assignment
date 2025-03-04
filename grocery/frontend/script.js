document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token'); // Получаем токен
    if (!token) {
        alert('Вы не авторизованы. Пожалуйста, войдите.');
        window.location.href = '/login/';
        return;
    }

    const cartItemsDiv = document.getElementById('cart-items');
    const totalPriceSpan = document.getElementById('total-price');
    const clearCartButton = document.getElementById('clear-cart');
    const addItemForm = document.getElementById('add-item-form');

    fetchCart();
    fetchCategories(); // Добавляем вызов для загрузки категорий

    async function fetchCategories() {
        try {
            const response = await fetch('/api/categories/');
            if (!response.ok) {
                throw new Error('Ошибка при загрузке категорий: ' + response.statusText);
            }
            const data = await response.json();
            renderCategories(data.results);
        } catch (error) {
            console.error(error);
            alert('Не удалось загрузить категории.');
        }
    }

    async function fetchSubCategories(categoryId) {
        try {
            const response = await fetch(`/api/subcategories/?category=${categoryId}`);
            if (!response.ok) {
                throw new Error('Ошибка при загрузке подкатегорий: ' + response.statusText);
            }
            const data = await response.json();
            renderSubCategories(data.results);
        } catch (error) {
            console.error(error);
            alert('Не удалось загрузить подкатегории.');
        }
    }

    async function fetchProducts(subCategoryId) {
        try {
            const response = await fetch(`/api/products/?sub_category=${subCategoryId}`);
            if (!response.ok) {
                throw new Error('Ошибка при загрузке продуктов: ' + response.statusText);
            }
            const data = await response.json();
            renderProducts(data.results);
        } catch (error) {
            console.error(error);
            alert('Не удалось загрузить продукты.');
        }
    }

    function renderCategories(categories) {
        const categoriesList = document.getElementById('categories-list');
        categoriesList.innerHTML = '';
        categories.forEach(category => {
            const categoryDiv = document.createElement('div');
            categoryDiv.innerHTML = `
                <img src="${category.image}" alt="${category.name}" style="width:100px;height:100px;">
                <span>${category.name}</span>
            `;
            categoryDiv.addEventListener('click', () => fetchSubCategories(category.id));
            categoriesList.appendChild(categoryDiv);
        });
    }

    function renderSubCategories(subCategories) {
        const subCategoriesList = document.getElementById('subcategories-list');
        subCategoriesList.innerHTML = '';
        subCategories.forEach(subCategory => {
            const subCategoryDiv = document.createElement('div');
            subCategoryDiv.innerHTML = `
                <img src="${subCategory.image}" alt="${subCategory.name}" style="width:100px;height:100px;">
                <span>${subCategory.name}</span>
            `;
            subCategoryDiv.addEventListener('click', () => fetchProducts(subCategory.id));
            subCategoriesList.appendChild(subCategoryDiv);
        });
    }

    function renderProducts(products) {
        const productsList = document.getElementById('products-list');
        productsList.innerHTML = '';
        products.forEach(product => {
            const productDiv = document.createElement('div');
            productDiv.innerHTML = `
                <img src="${product.image_small}" alt="${product.name}" style="width:100px;height:100px;">
                <span>${product.name}</span>
                <span>${product.price} руб.</span>
                <button class="add-to-cart" data-product="${product.name}" data-id="${product.id}">Добавить в корзину</button>
            `;
            productDiv.querySelector('.add-to-cart').addEventListener('click', () => {
                // Заполняем поле Название товара
                document.getElementById('product-name').value = product.name;
                // Заполняем поле Количество по умолчанию 1, если это нужно:
                document.getElementById('quantity').value = 1;
            });
            productsList.appendChild(productDiv);
        });
    }

    async function addToCart(productId) {
        try {
            const response = await fetch('/api/cart/add_item/', {
                method: 'POST',
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ product_id: productId })
            });

            if (!response.ok) {
                throw new Error('Ошибка при добавлении товара: ' + response.statusText);
            }

            alert('Товар добавлен в корзину.');
            fetchCart(); // Обновляем корзину после добавления товара
        } catch (error) {
            console.error(error);
            alert('Не удалось добавить товар.');
        }
    }

    // Функция для обновления отображения корзины
    async function fetchCart() {
        try {
            const response = await fetch('/api/cart/', {
                method: 'GET',
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                console.error('Ошибка:', response.status, response.statusText);
                alert('Не удалось загрузить корзину.');
                return;
            }

            const data = await response.json();
            console.log('Cart data:', data); // Вывод данных корзины в консоль для проверки
            renderCart(data);
        } catch (error) {
            console.error(error);
            alert('Не удалось загрузить корзину.');
        }
    }

    // Функция для отображения корзины
    function renderCart(cartData) {
        cartItemsDiv.innerHTML = '';
        let total = 0;

        if (cartData.results.length > 0) {
            const cart = cartData.results[0]; // Получаем первую корзину

            cart.items.forEach(item => {
                const itemDiv = document.createElement('div');
                itemDiv.classList.add('cart-item');

                itemDiv.innerHTML = `
                    <span>${item.product.name} (${item.quantity} шт.)</span>
                    <span>${(item.product.price * item.quantity).toFixed(2)} руб.</span>
                    <button class="update-item" data-product="${item.product.name}" data-quantity="${item.quantity}">Изменить</button>
                    <button class="remove-item" data-product="${item.product.name}">Удалить</button>
                `;

                cartItemsDiv.appendChild(itemDiv);
                total += item.product.price * item.quantity;
            });

            // Обновляем обработчики для кнопок
            addEventListenersToButtons();
        } else {
            cartItemsDiv.innerHTML = '<p>Корзина пуста.</p>';
        }

        totalPriceSpan.textContent = total.toFixed(2);
    }

    function addEventListenersToButtons() {
        document.querySelectorAll('.update-item').forEach(button => {
            button.addEventListener('click', handleUpdateItem);
        });

        document.querySelectorAll('.remove-item').forEach(button => {
            button.addEventListener('click', handleRemoveItem);
        });
    }

    async function handleUpdateItem(event) {
        const productName = event.target.getAttribute('data-product');
        const quantity = prompt('Введите новое количество:', event.target.getAttribute('data-quantity'));
        
        if (quantity !== null) {
            try {
                const response = await fetch('/api/cart/update_item/', {
                    method: 'POST',  // Измените на 'PUT', если API требует это
                    headers: {
                        'Authorization': `Token ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        product_name: productName,
                        quantity: parseInt(quantity)
                    })
                });
                
                if (!response.ok) {
                    throw new Error('Ошибка при обновлении товара: ' + response.statusText);
                }

                alert('Количество товара обновлено.');
                fetchCart();
            } catch (error) {
                console.error(error);
                alert('Не удалось обновить товар.');
            }
        }
    }

    async function handleRemoveItem(event) {
        const productName = event.target.getAttribute('data-product');

        if (confirm(`Вы уверены, что хотите удалить "${productName}" из корзины?`)) {
            try {
                const response = await fetch('/api/cart/remove_item/', {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Token ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        product_name: productName
                    })
                });

                if (!response.ok) {
                    throw new Error('Ошибка при удалении товара: ' + response.statusText);
                }

                alert('Товар удален из корзины.');
                fetchCart();
            } catch (error) {
                console.error(error);
                alert('Не удалось удалить товар.');
            }
        }
    }

    // Обработчик для очистки корзины
    clearCartButton.addEventListener('click', async () => {
        try {
            const response = await fetch('/api/cart/clear/', {
                method: 'DELETE',
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error('Ошибка при очистке корзины: ' + response.statusText);
            }

            alert('Корзина очищена.');
            fetchCart();
        } catch (error) {
            console.error(error);
            alert('Не удалось очистить корзину.');
        }
    });

    
    // Обработчик для добавления товара
    addItemForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const productName = document.getElementById('product-name').value;
        const quantity = document.getElementById('quantity').value;

        try {
            const response = await fetch('/api/cart/add_item/', {
                method: 'POST',
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    product_name: productName,
                    quantity: parseInt(quantity)
                })
            });

            if (!response.ok) {
                throw new Error('Ошибка при добавлении товара: ' + response.statusText);
            }

            alert('Товар добавлен в корзину.');
            fetchCart();
        } catch (error) {
            console.error(error);
            alert('Не удалось добавить товар.');
        }
    });

    // Инициализация
    fetchCart();
});