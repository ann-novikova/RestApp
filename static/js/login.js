document.getElementById('loginForm').onsubmit = async (e) => {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch("/users/api/token/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Если Django требует CSRF даже при логине:
                'X-CSRFToken': Auth.getCookie('csrftoken')
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Теперь Auth.save существует!
            Auth.save(data);

            alert("Вход выполнен успешно!");
            window.location.href = "/";
        } else {
            alert("Ошибка: " + (data.detail || "Неверный логин или пароль"));
        }
    } catch (err) {
        console.error("Ошибка сети:", err);
        alert("Не удалось связаться с сервером");
    }
};
