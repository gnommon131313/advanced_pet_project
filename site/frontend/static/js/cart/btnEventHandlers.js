export function attachButtonEvents() {
    const container = document.getElementById('order-create-btn');
    container.addEventListener('click', function(event) {
        console.log("Заказ успешно оформлен!");
        console.log(" 'не оформлен по настоящему т.к. логики нет' ");
    });
}