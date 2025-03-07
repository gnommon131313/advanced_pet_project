export function initializeOnContentLoaded() {
    fetch('http://localhost/api/catalog/products')
    .then(response => {
        if (!response.ok) {
            throw new Error('Не удалось загрузить данные');
        }
        return response.json();
    })
    .then(data => {
        const products = data;
        const newList = document.getElementById('catalog-list');

        console.log("data type =", typeof data); // несмотря на что response => response.json() тут тип все равно object, это особенности JS
        console.log(data);

        // Разбиваем на блоки по X элементов
        const row_number = 5
        for (let i = 0; i < products.length; i += row_number) {
            const row = document.createElement('div');
            row.classList.add('row', 'mb-4');

            // Отображаем 5 продуктов за раз
            for (let j = 0; j < row_number; j++) {
                if (i + j >= products.length) break; // если продуктов меньше 5 в последней строке
                
                const product = products[i + j];
                const productId = i + j + 1; // Достать нужный product_id

                // Создаем карточку для продукта
                const col = document.createElement('div');
                col.classList.add('col-md-2', 'mb-4');
                col.innerHTML = `
                    <div class="card">
                        <img src="https://via.placeholder.com/150" alt="Placeholder">
                        <div class="card-body">
                            <h5 class="card-title">${product.name}</h5>
                            <p class="card-text">${product.description}</p>
                            <p class="card-text"><strong>${product.price} ₽</strong></p>
                            <button class="btn btn-primary add-cart-product-btn" data-product-id=${productId}>add to cart</button>
                        </div>
                    </div>
                `;

                row.appendChild(col);
            }

            newList.appendChild(row);
        }
    })
    .catch(error => console.error('Ошибка при загрузке данных:', error));
}