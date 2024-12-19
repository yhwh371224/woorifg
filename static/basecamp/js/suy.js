document.addEventListener("DOMContentLoaded", function () {
    const masthead = document.querySelector("header.masthead");
    const images = [
        "/static/basecamp/assets/img/suy7.webp",
        "/static/basecamp/assets/img/suy8.webp",
        "/static/basecamp/assets/img/suy5.webp",
    ];
    let currentIndex = 0;

    function changeBackground() {
        masthead.style.backgroundImage = `url('${images[currentIndex]}')`;
        currentIndex = (currentIndex + 1) % images.length;
    }

    // 5초마다 배경 변경
    setInterval(changeBackground, 5000);
});

