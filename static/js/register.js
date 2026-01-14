document.getElementById('regForm').onsubmit = async (e) => {
    e.preventDefault();

    const payload = {
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        first_name: document.getElementById('first_name').value,
        last_name: document.getElementById('last_name').value,
        phone: document.getElementById('phone').value,
    };


    const response = await Auth.api('/users/api/register/', 'POST', payload);

    if (response && response.ok) {
        const data = await response.json();

        Auth.saveTokens(data);

        alert("Регистрация прошла успешно!");
        window.location.href = "/";
    } else if (response) {
        const errorData = await response.json();
        alert("Ошибка регистрации: " + JSON.stringify(errorData));
    } else {
        alert("Проблема с соединением");
    }
};