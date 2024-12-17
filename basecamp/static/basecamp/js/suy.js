const images = [
"{% static 'basecamp/assets/img/suy8.webp' %}",
"{% static 'basecamp/assets/img/suy7.webp' %}",
"{% static 'basecamp/assets/img/suy5.webp' %}" 
];

let currentIndex = 0; 

function changeBackgroundImage() {
const header = document.querySelector('header.masthead');          

header.style.backgroundImage = `url(${images[currentIndex]})`;          

currentIndex = (currentIndex + 1) % images.length;
}      

setInterval(changeBackgroundImage, 3000);

document.addEventListener('DOMContentLoaded', function() {
    // 모바일 환경에서만 적용
    if (window.innerWidth <= 767.95) {
        document.querySelectorAll('.dropdown-item').forEach(function(item) {
            item.addEventListener('click', function(e) {
                e.stopPropagation(); // 메뉴가 닫히지 않도록 방지
            });
        });
    }
});