document.addEventListener('DOMContentLoaded', () => {
    const html = document.documentElement;
    const themeToggleBtn = document.getElementById('theme-toggle');
    if (!themeToggleBtn) return;

    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        html.classList.add('dark');
        themeToggleBtn.textContent = '☀️';
    } else if (savedTheme === 'light') {
        html.classList.remove('dark');
        themeToggleBtn.textContent = '🌙';
    } else {
        // Ak nie je nič uložené, začni v light
        html.classList.remove('dark');
        themeToggleBtn.textContent = '🌙';
    }

    themeToggleBtn.addEventListener('click', () => {
        html.classList.toggle('dark');
        const isDark = html.classList.contains('dark');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
        themeToggleBtn.textContent = isDark ? '☀️' : '🌙';
    });
});
