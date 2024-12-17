document.addEventListener("DOMContentLoaded", function() {
    const images = [
        "{% static 'basecamp/assets/img/suy7.webp' %}",
        "{% static 'basecamp/assets/img/suy8.webp' %}",
        "{% static 'basecamp/assets/img/suy5.webp' %}"
    ];

    let currentIndex = 0;

    function changeBackgroundImage() {
        const header = document.querySelector('header.masthead');
        if (header) {
            const imgUrl = images[currentIndex];
            const img = new Image();
            img.src = imgUrl;

            img.onload = function() {
                header.style.opacity = 0;
                header.style.backgroundImage = `url(${imgUrl})`;

                setTimeout(function() {
                    header.classList.add("visible");
                }, 100); 
            };

            currentIndex = (currentIndex + 1) % images.length;
        }
    }

    setInterval(changeBackgroundImage, 3000);
});

