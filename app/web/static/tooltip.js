document.querySelectorAll('.aspect').forEach(el => {
    el.addEventListener('mouseenter', () => {
        const tip = el.querySelector('.tooltip');

        // Сброс всех прошлых сдвигов
        tip.style.left = '';
        tip.style.right = '';
        tip.style.top = '';
        tip.style.bottom = '';
        tip.style.transform = '';

        const rect = tip.getBoundingClientRect();

        // Вертикаль: не влезает сверху — показать снизу
        if (rect.top < 8) {
            tip.style.bottom = 'auto';
            tip.style.top = '100%';
            tip.style.marginBottom = '0';
            tip.style.marginTop = '0.4vw';
        }

        // Горизонталь (после вертикального сдвига пересчитать)
        const rect2 = tip.getBoundingClientRect();
        if (rect2.right > window.innerWidth - 8) {
            tip.style.left = 'auto';
            tip.style.right = '0';
            tip.style.transform = 'none';
        } else if (rect2.left < 8) {
            tip.style.left = '0';
            tip.style.transform = 'none';
        }
    });
});