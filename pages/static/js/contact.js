document.addEventListener('DOMContentLoaded', () => {
    const captchaImg = document.querySelector('.captcha');
    if (!captchaImg) return;

    const wrapper = document.createElement('div');
    wrapper.className = 'captcha-row';
    captchaImg.insertAdjacentElement('beforebegin', wrapper);
    wrapper.appendChild(captchaImg);

    const refreshBtn = document.createElement('button');
    refreshBtn.type = 'button';
    refreshBtn.className = 'captcha-refresh';
    refreshBtn.setAttribute('aria-label', 'Get a new captcha image');
    refreshBtn.innerHTML = '<i class="bi bi-arrow-clockwise"></i>';
    wrapper.appendChild(refreshBtn);

    refreshBtn.addEventListener('click', () => {
        fetch('/captcha/refresh/', { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
            .then((res) => res.json())
            .then((data) => {
                captchaImg.src = data.image_url;
                document.getElementById('id_captcha_0').value = data.key;
                document.getElementById('id_captcha_1').value = '';
            });
    });
});
