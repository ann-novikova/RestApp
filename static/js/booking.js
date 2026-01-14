let selectedTableId = null;
const tableCoords = [
    {r: 1, c: 1}, {r: 1, c: 3}, {r: 1, c: 5},
    {r: 3, c: 1}, {r: 6, c: 3}, {r: 6, c: 5}, {r: 6, c: 1}
];

/**
 * 1. ИНИЦИАЛИЗАЦИЯ
 */
document.addEventListener('DOMContentLoaded', () => {
    // Предзаполняем данные пользователя, если он авторизован
    preloadUserData();

    // Авто-подсчет времени окончания (+2 часа)
    const timeInput = document.getElementById('book-time');
    if (timeInput) {
        timeInput.addEventListener('change', function() {
            let t = this.value.split(':');
            let h = (parseInt(t[0]) + 2) % 24;
            document.getElementById('book-end-time').value = (h < 10 ? '0' + h : h) + ':' + t[1];
        });
    }
});

/**
 * 2. ЛОГИКА ИНТЕРФЕЙСА (ШАГИ)
 */
function showStep(s) {
    ['step-1', 'step-2', 'step-3', 'step-success'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.classList.add('hidden');
    });
    const currentStep = document.getElementById('step-' + s);
    if (currentStep) currentStep.classList.remove('hidden');
}

function clearErrors() {
    document.querySelectorAll('.error-message').forEach(span => {
        span.innerText = '';
        span.style.display = 'none';
    });
    const dateErrorBlock = document.getElementById('date-error');
    if (dateErrorBlock) {
        dateErrorBlock.innerText = '';
        dateErrorBlock.style.display = 'none';
    }
}

 function displayErrors(errors) {
        clearErrors();
        if (!errors) return;

        for (const fieldName in errors) {
            const errorSpan = document.getElementById(`error-${fieldName}`);
            if (errorSpan && errors[fieldName].length > 0) {
                errorSpan.innerText = errors[fieldName][0];
                errorSpan.style.color = '#dc3545';
                errorSpan.style.display = 'block';
            }
        }

        if (errors.non_field_errors && errors.non_field_errors.length > 0) {
             const dateErrorBlock = document.getElementById('date-error');
             if (dateErrorBlock) {
                 dateErrorBlock.innerText = errors.non_field_errors[0];
                 dateErrorBlock.style.display = 'block';
             }
        } else if (errors.error) { // Обработка общего сообщения об ошибке
             const dateErrorBlock = document.getElementById('date-error');
             if (dateErrorBlock) {
                 dateErrorBlock.innerText = errors.error;
                 dateErrorBlock.style.display = 'block';
             }
        }
    }

/**
 * 3. РАБОТА С API
 */

// Предзагрузка данных профиля
async function preloadUserData() {
    const token = localStorage.getItem('access_token');
    if (!token) return;

    try {
        const response = await Auth.api('/users/profile/api/');
        if (response && response.ok) {
            const userData = await response.json();
            if (userData.first_name) document.getElementById('cust-name').value = userData.first_name;
            if (userData.phone) document.getElementById('cust-phone').value = userData.phone;
        }
    } catch (err) {
        console.error("Ошибка при предзагрузке профиля:", err);
    }
}

// ШАГ 1: Проверка доступности
async function checkAvailability() {
    clearErrors();
    const date = document.getElementById('book-date').value;
    const start = document.getElementById('book-time').value;
    const end = document.getElementById('book-end-time').value;

    try {
        const response = await fetch(`/bookings/check/?date=${date}&start=${start}&end=${end}`);
        const data = await response.json();

        if (response.ok) {
            renderTables(data.tables, date, start, end);
            showStep(2);
        } else {
            displayErrors(data.errors || data);
        }
    } catch (err) {
        console.error("Ошибка в checkAvailability:", err);
    }
}

// ШАГ 2: Отрисовка столов
function renderTables(tables, date, start, end) {
    const floor = document.getElementById('floor-plan');
    floor.querySelectorAll('.table-wrapper').forEach(el => el.remove());

    tables.slice(0, tableCoords.length).forEach((table, index) => {
        const pos = tableCoords[index];
        const wrapper = document.createElement('div');
        wrapper.className = 'table-wrapper';
        wrapper.style.gridRow = pos.r;
        wrapper.style.gridColumn = pos.c;

        let sizeClass = table.capacity <= 2 ? 'size-sm' : (table.capacity >= 5 ? 'size-lg' : 'size-md');
        const statusClass = table.is_available ? 'available' : 'occupied';

        wrapper.innerHTML = `
            <div class="table-circle ${sizeClass} ${statusClass}">
                <span class="table-number">№${table.number}</span>
                <span class="table-capacity">${table.capacity} чел</span>
            </div>
        `;

        if (table.is_available) {
            wrapper.onclick = () => {
                selectedTableId = table.id;
                document.getElementById('summary').innerText = `СТОЛ №${table.number} | ${date} | ${start} - ${end}`;
                showStep(3);
            };
        }
        floor.appendChild(wrapper);
    });
}

// ШАГ 3: Отправка формы бронирования
document.getElementById('booking-form').onsubmit = async function(e) {
    e.preventDefault();
    clearErrors();

    if (!selectedTableId) {
        alert("Пожалуйста, выберите столик на схеме.");
        return;
    }

    const date = document.getElementById('book-date').value;
    const payload = {
        table: selectedTableId,
        start_time: date + 'T' + document.getElementById('book-time').value,
        end_time: date + 'T' + document.getElementById('book-end-time').value,
        guests_count: document.getElementById('cust-guests').value,
        customer_name: document.getElementById('cust-name').value,
        customer_phone: document.getElementById('cust-phone').value,
        comment: document.getElementById('cust-comment').value
    };

    try {
        // Используем Auth.api для автоматической обработки токенов и CSRF
        const response = await Auth.api('/bookings/create/', 'POST', payload);

        if (response && response.ok) {
            showStep('success');
        } else {
            const data = await response.json();
            displayErrors(data.errors || data);
        }
    } catch (err) {
        alert("Произошла ошибка при отправке запроса");
        console.error(err);
    }
};
