export function attachButtonEvents() {
    let tg = window.Telegram.WebApp;
    const user = tg.initDataUnsafe.user;
    // const userId = user.id;
    const userId = 666; // Для теста вне mini app, т.к. нельзя получить tg.initDataUnsafe.user и нету регистрации

    // Вешаем обработчик на родительский элемент (нужно именно вешать обработчик на родительский обьект а не просто пытаться получать все кнопки с нужным id или class, тк они могут быть созданы динамически и не будут обработаны когда скрипт запуститься и не найдет их сразу)
    const container = document.getElementById('catalog-list');
    container.addEventListener('click', function(event) {
        // Проверяем, что клик произошел на кнопке с нужным классом
        // Проверять лучше именно по классу, т.к. id привязан к конкретному экземпляру и не может повторяться
        if (event.target && event.target.classList.contains('add-cart-product-btn')) {
            // Логика обработки клика
            const productId = event.target.getAttribute('data-product-id'); // Получение значений из переданных атрибутов
            event.target.style.display = "none"; // Скрыть кнопку, т.к. нужно ждать ответ от сервера, а многократные клики могут вызвать ошибки, т.к. сервер не успеет обрабоать предыдущие запросы
            console.log('Клик по кнопке для товара с ID:', productId);

            // Отправка данных на сервер
            const data = {
                productId: productId,
            };

            fetch(`http://localhost/api/carts/products/${userId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json', // Указываем, что отправляем данные в формате JSON
                },
                body: JSON.stringify(data), // Эти данные будут переданы в аргументы функции, которую декарирует FastApi
            })
            .then(response => response.json())
            .then(responseData => {
                // alert("Ответ от сервера: " + JSON.stringify(responseData));
                
                event.target.style.display = "inline-block"; // Снова показать кнопку после получения ответа от сервера
            })
            .catch(error => {
                console.error('Ошибка:', error);
            });
        }
    });
}