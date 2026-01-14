// Используем window.Auth чтобы объект был глобально доступен
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

    // Переименовали из saveTokens в save
    save(data) {
        if (data.access) localStorage.setItem('access_token', data.access);
        if (data.refresh) localStorage.setItem('refresh_token', data.refresh);
    },

    logout() {
        localStorage.clear();
        window.location.href = '/users/login/';
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
            'X-CSRFToken': this.getCookie('csrftoken') // используем this
        };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const options = { method, headers };
        if (body) options.body = JSON.stringify(body);

        let response = await fetch(url, options);

        if (response.status === 401 && localStorage.getItem('refresh_token')) {
            const refreshed = await this.refreshToken();
            if (refreshed) {
                return this.api(url, method, body);
            } else {
                this.logout();
            }
        }
        return response;
    },

    async refreshToken() {
        const refresh = localStorage.getItem('refresh_token');
        const res = await fetch('/users/token/refresh/', {
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

document.addEventListener('DOMContentLoaded', () => Auth.updateNavbar());
