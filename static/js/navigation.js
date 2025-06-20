document.addEventListener('DOMContentLoaded', function() {
    const currentLocation = window.location.pathname;
    console.log('Current Location:', currentLocation);

    const navLinks = document.querySelectorAll('nav a');
    console.log('Nav Links:', navLinks);

    navLinks.forEach(link => {
        console.log('Link Href:', link.href);
        // Проверка, что элемент не является кнопкой "Выйти"
        if (!link.classList.contains('logoutButton') && link.href.includes(currentLocation)) {
            link.classList.add('active');
        }
    });
});
