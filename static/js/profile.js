/**
 • ЛОГИКА ИНТЕРФЕЙСА
 */

// Переключение между режимом чтения и редактирования
async function preloadContactForm() {
    // Проверяем, существует ли access_token, чтобы не делать лишних запросов
    const token = localStorage.getItem('access_token');
    if (!token) return;

    try {
        // Используем универсальный метод из auth.js
        const response = await Auth.api('/users/profile/api/');

        if (response && response.ok) {
            const data = await response.json();

            // Заполняем поля формы обратной связи, если они существуют
            const nameField = document.getElementById('id_name'); // id_name - это стандартный id от Django
            const emailField = document.getElementById('id_email'); // id_email - это стандартный id от Django

            if (nameField && data.first_name) {
                nameField.value = data.first_name;
            }
            // Если у вас есть last_name и вы хотите его добавить к имени
            if (nameField && data.last_name && data.first_name) {
                nameField.value = `${data.first_name} ${data.last_name}`;
            } else if (nameField && data.last_name) {
                nameField.value = data.last_name;
            }

            if (emailField && data.email) {
                emailField.value = data.email;
            }
        }
        // Если response.status === 401, Auth.api сам позаботится о refreshToken или logout
    } catch (err) {
        console.error("Ошибка при предзагрузке формы обратной связи:", err);
    }
}


// Запуск при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    // Запускаем предзагрузку профиля (для страницы профиля)
    loadProfile();

    // НОВОЕ: Запускаем предзагрузку формы обратной связи (для главной страницы)
    preloadContactForm();
});

function toggleEdit(isEditing) {
    const profileActions = document.getElementById('profile-actions');
    const editActions = document.getElementById('edit-actions');
    const inputs = ['user-first-name', 'user-last-name', 'user-phone'];

    if (isEditing) {
        profileActions.classList.add('d-none');
        editActions.classList.remove('d-none');
        inputs.forEach(id => {
            const el = document.getElementById(id);
            el.disabled = false;
            el.style.border = '1px solid #d4af37';
            el.style.background = 'rgba(255,255,255,0.1)';
        });
    } else {
        profileActions.classList.remove('d-none');
        editActions.classList.add('d-none');
        inputs.forEach(id => {
            const el = document.getElementById(id);
            el.disabled = true;
            el.style.border = '1px solid rgba(212,175,55,0.2)';
            el.style.background = 'rgba(255,255,255,0.05)';
        });
        loadProfile(); // Откат изменений при отмене
    }
}

/**
 • РАБОТА С API
 */

// Загрузка данных профиля и списка бронирований
async function loadProfile() {
    const token = localStorage.getItem('access_token');
    if (!token) return;

    const statusLabels = {
        'pending': { label: 'В работе', color: '#ffc107' },
        'confirmed': { label: 'Подтверждено', color: '#28a745' },
        'cancelled': { label: 'Отменено', color: '#dc3545' }
    };

    try {
        const response = await Auth.api('/users/profile/api/');

        if (response && response.ok) {
            const data = await response.json();

            const firstNameEl = document.getElementById('user-first-name');
            if (firstNameEl) {
                firstNameEl.value = data.first_name || '';
                document.getElementById('user-last-name').value = data.last_name || '';
                document.getElementById('user-phone').value = data.phone || '';
                document.getElementById('user-email').value = data.email || '';

                renderBookings(data.bookings, statusLabels);
            }
        }
    } catch (err) {
        console.error("Ошибка при загрузке данных:", err);
    }
}


function renderBookings(bookings, statusLabels) {
    const container = document.getElementById('bookings-container');
    if (bookings && bookings.length > 0) {
        container.innerHTML = bookings.map(b => {
            const status = statusLabels[b.status] || { label: b.status, color: '#d4af37' };
            const bookingDate = new Date(b.start_time).toLocaleString('ru-RU', {
                day: '2-digit', month: '2-digit', year: 'numeric',
                hour: '2-digit', minute: '2-digit'
            });

            return `
            <div class="booking-item p-3 mb-3" style="border-left: 2px solid #d4af37; background: rgba(255,255,255,0.02);">
                <div class="row align-items-center w-100 g-0">
                    <div class="col-md-3 col-6 text-start">
                        <div class="text-white fw-bold">СТОЛ №${b.table_number || b.table}</div>
                        <div style="font-size: 0.7rem; color: #6c757d; text-transform: uppercase;">${b.guests_count} гостей</div>
                    </div>
                    <div class="col-md-5 col-6 text-center text-md-start">
                        <label class="small d-block mb-1" style="font-size: 0.65rem; text-transform: uppercase; color: #d4af37;">Дата и время</label>
                        <div class="small text-white">${bookingDate}</div>
                    </div>
                    <div class="col-md-4 col-12 text-md-end text-start mt-2 mt-md-0">
                        <label class="small d-block mb-1" style="font-size: 0.65rem; text-transform: uppercase; color: #d4af37;">Статус</label>
                        <span style="border: 1px solid ${status.color}; color: ${status.color}; padding: 4px 12px; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px;">
                            ${status.label}
                        </span>
                    </div>
                </div>
            </div>`;
        }).join('');
    } else {
        container.innerHTML = '<p class="text-gold italic">У вас пока нет активных бронирований.</p>';
    }
}

// Сохранение профиля
async function saveProfile() {
    const updatedData = {
        first_name: document.getElementById('user-first-name').value,
        last_name: document.getElementById('user-last-name').value, // добавил фамилию, раз она есть в форме
        phone: document.getElementById('user-phone').value
    };

    try {
        // Auth.api сам добавит токен и X-CSRFToken
        const response = await Auth.api('/users/profile/update/', 'PATCH', updatedData);

        if (response && response.ok) {
            toggleEdit(false);
            alert("Данные успешно сохранены");
        } else {
            const errData = await response.json();
            alert("Ошибка сохранения: " + JSON.stringify(errData));
        }
    } catch (err) {
        alert("Ошибка сети при попытке сохранения");
    }
}

// Запуск при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');

    if (token) {
        loadProfile();

        if (document.getElementById('id_name')) {
            preloadContactForm();
        }
    }
});
