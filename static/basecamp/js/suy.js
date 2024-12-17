document.addEventListener("DOMContentLoaded", function() {
    const images = [
        "/static/basecamp/assets/img/suy7.webp",  
        "/static/basecamp/assets/img/suy8.webp",
        "/static/basecamp/assets/img/suy5.webp"
    ];

    let currentIndex = 0;

    function changeBackgroundImage() {
        const header = document.querySelector('header.masthead');
        if (header) {
            header.style.backgroundImage = `url(${images[currentIndex]})`;
            currentIndex = (currentIndex + 1) % images.length;
        }
    }

    setInterval(changeBackgroundImage, 3000);
});

