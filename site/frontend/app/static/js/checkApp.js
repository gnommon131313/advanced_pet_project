export function isTgWebApp() {
    // Проверка на запуск сайта внутри телеграма (через Mini Apps)(нужно т.к. нету кастомной регистрации а многие функции требую идентифицировать пользователя, например ID)
    if (window.Telegram && window.Telegram.WebApp) {
        let tg = window.Telegram.WebApp;
        const user = tg.initDataUnsafe.user;
        
        // Если не удалось получить данные о пользователе значит приложение запущено вне mini apps, нужно избегать т.к. часто аутентификация происходит по tg.initDataUnsafe.user.id
        if (user) {
            return true;
        } else {
            alert("this application was launched outside the zone 'Tg Mini App'");
            return false;
        }
    } else {
        alert('WebApp not found');
        return false;
    }
}
