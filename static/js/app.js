document.addEventListener('DOMContentLoaded', function() {
    // Динамическое добавление скрипта
    var script = document.createElement('script');
    script.src= "/static/js/app.js"; 
    script.onload = function() {
        console.log('Скрипт успешно загружен');
    };
    script.onerror = function() {
        console.error('Ошибка при загрузке скрипта');
    };
    document.head.appendChild(script);

    const loginForm = document.querySelector('form');
    const logoutButton = document.getElementById('logoutButton');
    const profileForm = document.getElementById('profileForm');
    const profilePictureInput = document.getElementById('profilePictureInput');
    const cropModal = document.getElementById('cropModal');
    const cropCanvas = document.getElementById('cropCanvas');
    const zoomRange = document.getElementById('zoomRange');
    const ctx = cropCanvas.getContext('2d');
    let img = new Image();
    let scale = 1;
    let inactivityTimeout;
    const inactivityDuration = 60 * 60 * 1000;

    // Пример отправки данных в API для входа
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const login = document.getElementById('login').value;
            const password = document.getElementById('password').value;

            fetch('http://127.0.0.1:5000/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ login: login, password: password })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Перенаправление на страницу профиля
                    window.location.href = 'user_panel';
                } else {
                    alert('Неверный логин или пароль');
                }
            })
            .catch(error => console.error('Error logging in:', error));
        });
    }

    // Пример отправки данных в API для выхода
    if (logoutButton) {
        logoutButton.addEventListener('click', function(event) {
            event.preventDefault();

            fetch('http://127.0.0.1:5000/api/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Перенаправление на страницу логина
                    window.location.href = 'login.html';
                } else {
                    alert('Ошибка при выходе');
                }
            })
            .catch(error => console.error('Error logging out:', error));
        });
    }

    // Обработка навигации
    document.querySelector('.account-link').addEventListener('click', function(event) {
        event.preventDefault();
        fetch('/api/user_data')
            .then(response => response.json())
            .then(data => {
                if (data.surname) {
                    // Пользователь авторизован, перенаправление на страницу профиля
                    window.location.href = 'user_panel';
                } else {
                    // Пользователь не авторизован, перенаправление на страницу логина
                    window.location.href = 'login.html';
                }
            })
            .catch(error => console.error('Error checking user data:', error));
    });

    // Пример отправки данных в API для обновления профиля
    if (profileForm) {
        profileForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(profileForm);

            fetch('http://127.0.0.1:5000/api/update_profile', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Профиль успешно обновлен');
                } else {
                    alert('Ошибка при обновлении профиля');
                }
            })
            .catch(error => console.error('Error updating profile:', error));
        });
    }

    // Пример отправки данных в API для загрузки медиа
    const mediaForm = document.getElementById('mediaForm');
    if (mediaForm) {
        mediaForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(mediaForm);

            fetch('http://127.0.0.1:5000/api/upload_media', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Медиа успешно загружено');
                } else {
                    alert('Ошибка при загрузке медиа');
                }
            })
            .catch(error => console.error('Error uploading media:', error));
        });
    }

    // Пример отправки данных в API для добавления команды
    const teamForm = document.getElementById('teamForm');
    const sportTypeSelect = teamForm ? teamForm.querySelector('select[name="sport_type"]') : null;
    const teamMembersContainer = document.getElementById('team_members_container');

    function updateTeamMembers() {
        if (sportTypeSelect && teamMembersContainer) {
            const sportType = sportTypeSelect.value;
            let memberCount;
            if (sportType === "football") { memberCount = 5; }
            else if (sportType === "basketball") { memberCount = 3; }
            else if (sportType === "volleyball") { memberCount = 6; }
            else { memberCount = 1; }

            teamMembersContainer.innerHTML = '';
            for (let i = 1; i <= memberCount; i++) {
                const input = document.createElement("input");
                input.type = "text";
                input.name = "team_members[]";
                input.placeholder = `Игрок команды ${i}`;
                input.required = true;
                teamMembersContainer.appendChild(input);
                teamMembersContainer.appendChild(document.createElement("br"));
            }
        }
    }

    if (sportTypeSelect) {
        sportTypeSelect.addEventListener('change', updateTeamMembers);
    }
    updateTeamMembers(); // Initial call to set the default members

    if (teamForm) {
        teamForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(teamForm);

            fetch('http://127.0.0.1:5000/api/add_team', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Команда успешно добавлена');
                } else {
                    alert('Ошибка при добавлении команды');
                }
            })
            .catch(error => console.error('Error adding team:', error));
        });
    }

    // Пример отправки данных в API для добавления физорга
    const physOrgForm = document.getElementById('physOrgForm');
    if (physOrgForm) {
        physOrgForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(physOrgForm);

            fetch('http://127.0.0.1:5000/api/add_physorg', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Физорг успешно добавлен');
                    physOrgForm.reset(); // Сброс формы
                } else {
                    alert('Ошибка при добавлении физорга');
                }
            })
            .catch(error => console.error('Ошибка при добавлении физорга:', error));
        });
    }

    // Пример отправки данных в API для добавления мероприятия
    const eventForm = document.getElementById('eventForm');
    const eventTypeSelect = eventForm ? eventForm.querySelector('select[name="event_type"]') : null;
    const sportsFields = document.getElementById('sportsFields');
    const commonFields = document.getElementById('commonFields');

    function toggleEventTypeFields() {
        if (eventTypeSelect && sportsFields && commonFields) {
            const eventType = eventTypeSelect.value;
            if (eventType === 'sports') {
                sportsFields.style.display = 'block';
                commonFields.style.display = 'block';
            } else {
                sportsFields.style.display = 'none';
                commonFields.style.display = 'block';
            }
        }
    }

    if (eventTypeSelect) {
        eventTypeSelect.addEventListener('change', toggleEventTypeFields);
    }
    toggleEventTypeFields(); // Initial call to set the default fields

    if (eventForm) {
        eventForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(eventForm);

            fetch('http://127.0.0.1:5000/api/add_event', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Мероприятие успешно добавлено');
                } else {
                    alert('Ошибка при добавлении мероприятия');
                }
            })
            .catch(error => console.error('Error adding event:', error));
        });
    }

    // Пример отправки данных в API для редактирования расписания тренировок
    const editTrainingScheduleForm = document.getElementById('editTrainingScheduleForm');
    if (editTrainingScheduleForm) {
        editTrainingScheduleForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(editTrainingScheduleForm);

            fetch('http://127.0.0.1:5000/api/edit_schedule', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Расписание тренировок успешно обновлено');
                } else {
                    alert('Ошибка при обновлении расписания тренировок');
                }
            })
            .catch(error => console.error('Error updating schedule:', error));
        });
    }

    // Обработка отправки формы добавления новости
    const addNewsForm = document.getElementById('addNewsForm');
    if (addNewsForm) {
        addNewsForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(addNewsForm);

            // Логирование данных формы перед отправкой
            for (let pair of formData.entries()) {
                console.log(pair[0] + ': ' + pair[1]);
            }

            fetch('/api/add_news', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    console.log('Новость успешно добавлена');
                    addNewsForm.reset();
                    window.location.href = '/'; // Перенаправление на страницу index.html
                } else {
                    console.error('Ошибка при добавлении новости:', data.error);
                }
            })
            .catch(error => console.error('Ошибка при добавлении новости:', error));
        });
    }

    // Загрузка новостей
    function fetchNews() {
        fetch('/api/get_news', {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => {
            console.log('Полученные новости:', data.news);
            const newsContainer = document.getElementById('news-container');
            if (newsContainer) {
                newsContainer.innerHTML = '';
                data.news.forEach(news => {
                    const newsCard = document.createElement('div');
                    newsCard.className = 'news_card';
                    newsCard.innerHTML = `
                        <h2>${news.title}</h2>
                        ${news.image ? `<img src="${news.image}" alt="Image" style="max-width: 100%; max-height: 200px;">` : ''}
                        <button class="read-more-button" data-news-id="${news.id}">Подробнее</button>
                    `;
                    newsContainer.appendChild(newsCard);
                });

                document.querySelectorAll('.read-more-button').forEach(button => {
                    button.addEventListener('click', function() {
                        const newsId = button.getAttribute('data-news-id');
                        fetch(`/api/get_news_by_id/${newsId}`)
                            .then(response => response.json())
                            .then(news => {
                                const modalTitle = document.getElementById('modalTitle');
                                const modalContent = document.getElementById('modalContent');
                                const modalImage1 = document.getElementById('modalImage1');
                                if (modalTitle) modalTitle.textContent = news.title;
                                if (modalContent) modalContent.textContent = news.description;
                                if (modalImage1) {
                                    modalImage1.src = news.image || '';
                                    modalImage1.style.display = news.image ? 'block' : 'none';
                                }
                                const newsModal = document.getElementById('newsModal');
                                if (newsModal) newsModal.style.display = 'block';
                            });
                    });
                });
            }
        })
        .catch(error => console.error('Error fetching news data:', error));
    }

    // Function to close the modal
    function closeModal() {
        const newsModal = document.getElementById('newsModal');
        if (newsModal) newsModal.style.display = 'none';
    }

    // Close the modal if the user clicks outside of it
    window.onclick = function(event) {
        const modal = document.getElementById('newsModal');
        if (modal && event.target === modal) {
            closeModal();
        }
    }

    // Пример вызова функции для получения новостей при загрузке страницы
    fetchNews();

    // Загрузка данных пользователя
    fetch('/api/user_data')
        .then(response => response.json())
        .then(data => {
            if (data.surname) {
                const surnameElement = document.getElementById('surname');
                if (surnameElement) surnameElement.textContent = data.surname;
            }
            if (data.name) {
                const firstNameElement = document.getElementById('first_name');
                if (firstNameElement) firstNameElement.textContent = data.name;
            }
            if (data.patronymic) {
                const middleNameElement = document.getElementById('middle_name');
                if (middleNameElement) middleNameElement.textContent = data.patronymic;
            }
            if (data.gender) {
                const genderElement = document.getElementById('gender');
                if (genderElement) genderElement.textContent = data.gender;
            }
            if (data.group) {
                const groupElement = document.getElementById('group');
                if (groupElement) groupElement.textContent = data.group;
            }
            if (data.role) {
                const roleElement = document.getElementById('role');
                if (roleElement) roleElement.textContent = data.role;
            }
        })
        .catch(error => console.error('Error fetching user data:', error));

    // Загрузка фото профиля
    fetch('/api/profile_picture')
        .then(response => {
            if (response.ok) {
                return response.blob();
            }
            throw new Error('Network response was not ok.');
        })
        .then(blob => {
            const url = URL.createObjectURL(blob);
            const previewImage = document.getElementById('previewImage');
            if (previewImage) {
                previewImage.src = url;
            }
        })
        .catch(error => console.error('Error fetching profile picture:', error));

    // Обработка изменения фото профиля
    profilePictureInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        const reader = new FileReader();

        reader.onload = function(e) {
            img.src = e.target.result;
            img.onload = function() {
                cropCanvas.width = 300;
                cropCanvas.height = 300;
                drawImage();
                cropModal.style.display = 'block';
            };
        };

        reader.readAsDataURL(file);
    });

    zoomRange.addEventListener('input', function() {
        scale = zoomRange.value;
        drawImage();
    });

    function drawImage() {
        const canvasWidth = cropCanvas.width;
        const canvasHeight = cropCanvas.height;
        const imgWidth = img.width * scale;
        const imgHeight = img.height * scale;
        const x = (canvasWidth - imgWidth) / 2;
        const y = (canvasHeight - imgHeight) / 2;

        ctx.clearRect(0, 0, canvasWidth, canvasHeight);
        ctx.drawImage(img, x, y, imgWidth, imgHeight);
    }

    function saveCroppedImage() {
        const croppedImage = cropCanvas.toDataURL('image/jpeg');
        const formData = new FormData();
        formData.append('profile_picture', croppedImage);

        fetch('/api/profile_picture', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('Error updating profile picture');
            }
        })
        .catch(error => console.error('Error updating profile picture:', error));

        closeCropModal();
    }

    function closeCropModal() {
        cropModal.style.display = 'none';
    }

    window.onclick = function(event) {
        if (event.target === cropModal) {
            closeCropModal();
        }
    };

    // Установка таймера для автоматического выхода
    function startInactivityTimer() {
        inactivityTimeout = setTimeout(logoutDueToInactivity, inactivityDuration);
    }

    function resetInactivityTimer() {
        clearTimeout(inactivityTimeout);
        startInactivityTimer();
    }

    function logoutDueToInactivity() {
        fetch('http://127.0.0.1:5000/api/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = 'login.html';
            } else {
                alert('Ошибка при автоматическом выходе');
            }
        })
        .catch(error => console.error('Error logging out due to inactivity:', error));
    }

    // Сброс таймера при активности пользователя
    document.addEventListener('mousemove', resetInactivityTimer);
    document.addEventListener('keypress', resetInactivityTimer);
    document.addEventListener('click', resetInactivityTimer);

    // Запуск таймера при загрузке страницы
    startInactivityTimer();

    // Добавление функционала удаления фото из профиля
    const deleteProfilePictureButton = document.getElementById('deleteProfilePictureButton');
    if (deleteProfilePictureButton) {
        deleteProfilePictureButton.addEventListener('click', function(event) {
            event.preventDefault();

            fetch('http://127.0.0.1:5000/api/delete_profile_picture', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const previewImage = document.getElementById('previewImage');
                    if (previewImage) {
                        previewImage.src = 'static/style/icon-placeholder.png'; // Установка иконки по умолчанию
                    }
                } else {
                    alert('Ошибка при удалении фото профиля');
                }
            })
            .catch(error => console.error('Error deleting profile picture:', error));
        });
    }
});
