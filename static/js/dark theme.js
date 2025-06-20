document.addEventListener('DOMContentLoaded', function() {
  const themeToggle = document.getElementById('theme-toggle');
  const themeIcon = document.getElementById('theme-icon');

  themeToggle.addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');

    if (document.body.classList.contains('dark-mode')) {
      themeIcon.src = 'static/style/Dark Mode.png'; // 
      themeIcon.alt = 'Иконка тёмной темы';
    } else {
      themeIcon.src = 'static/style/White Mode.png'; 
      themeIcon.alt = 'Иконка светлой темы';
    }
  });
});
