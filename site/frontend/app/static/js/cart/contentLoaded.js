export function initializeOnContentLoaded() {
    let tg = window.Telegram.WebApp;
    const user = tg.initDataUnsafe.user;
    // const userId = user.id;
    const userId = 666; // Для теста вне mini app, т.к. нельзя получить tg.initDataUnsafe.user и нету регистрации чтобы идентифицировать пользователей

    fetch(`http://localhost/api/carts/products/${userId}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Не удалось загрузить данные');
        }
        return response.json();
    })
    .then(data => {
        // Вывод в консоль браузера (F12 что посмотреть)
        console.log(data);
        
        var totalPrice = 0
        
        if (Array.isArray(data) && data !== null) {
            if (data.length > 0) {
                // Расчитать Total Price
                for (let i = 0; i < data.length; i++) {
                    totalPrice += data[i].total;
                }

                // Скрыть кнопку если не товаров в карзине
                var order_create_btn = document.getElementById("order-create-btn");
                order_create_btn.style.display = "inline-block";
            }
        }

        // Очищаем таблицу перед добавлением новых данных
        const newList = document.getElementById('carts-list');
        newList.innerHTML = '';

        // Заполняем таблицу полученными данными
        data.forEach(function(element) {
            let row = `<tr>
                <td>${element.cart_id}</td>
                <td>${element.product_id}</td>
                <td>${element.quantity}</td>
                <td>${element.total}</td>
            </tr>`;
            newList.insertAdjacentHTML('beforeend', row);
        });

        // Записать Total Price
        const priceList = document.getElementById('carts-total-price');
        priceList.innerHTML = '';
        let priceRow = `<tr>
            <td>${totalPrice}</td>
        </tr>`;
        priceList.insertAdjacentHTML('beforeend', priceRow);
    })
    .catch(error => {
        alert(error.message);
    });
}