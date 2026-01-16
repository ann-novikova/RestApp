window.Auth = {
    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },

    save(data) {
        if (data.access) localStorage.setItem('access_token', data.access);
        if (data.refresh) localStorage.setItem('refresh_token', data.refresh);
    },

    logout(shouldRedirect = true) {
        localStorage.clear();
        if (shouldRedirect) {
            window.location.href = '/users/login/';
        } else {
            this.updateNavbar();
        }
    },

    updateNavbar() {
        const token = localStorage.getItem('access_token');
        const guestEls = document.querySelectorAll('.nav-guest');
        const userEls = document.querySelectorAll('.nav-user');

        if (token) {
            guestEls.forEach(el => el.classList.add('d-none'));
            userEls.forEach(el => el.classList.remove('d-none'));
        } else {
            guestEls.forEach(el => el.classList.remove('d-none'));
            userEls.forEach(el => el.classList.add('d-none'));
        }
    },

    async api(url, method = 'GET', body = null) {
        const token = localStorage.getItem('access_token');
        const headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCookie('csrftoken')
        };
        // ИСПРАВЛЕНО: Добавлены обратные кавычки
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const options = { method, headers };
        if (body) options.body = JSON.stringify(body);

        let response = await fetch(url, options);

        if (response.status === 401 && localStorage.getItem('refresh_token')) {
            const refreshed = await this.refreshToken();
            if (refreshed) {
                return this.api(url, method, body);
            } else {
                this.logout(false); // ИСПРАВЛЕНО: Не редиректим
            }
        }
        return response;
    },

    async refreshToken() {
        const refresh = localStorage.getItem('refresh_token');
        if (!refresh) return false;        const res = await fetch('/users/token/refresh/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCookie('csrftoken')
            },
            body: JSON.stringify({ refresh })
        });
        if (res.ok) {
            const data = await res.json();
            localStorage.setItem('access_token', data.access);
            return true;
        }
        return false;
    }
};

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    Auth.updateNavbar();

    // ИСПРАВЛЕНО: Проверка наличия формы перед установкой обработчика
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.onsubmit = async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            try {
                const response = await fetch("/users/api/token/", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': Auth.getCookie('csrftoken')
                    },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();
                if (response.ok) {
                    Auth.save(data);
                    window.location.href = "/";
                } else {
                    alert("Ошибка: " + (data.detail || "Неверный логин или пароль"));
                }
            } catch (err) {
                console.error("Ошибка сети:", err);
            }
        };
    }
});
