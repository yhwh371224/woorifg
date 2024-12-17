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

// Bootstrap 5 JavaScript로 설정
var dropdowns = document.querySelectorAll('.dropdown-toggle');

dropdowns.forEach(function(dropdown) {
    dropdown.addEventListener('click', function (event) {
        var menu = this.nextElementSibling;
        if (window.innerWidth <= 767.95) {
            event.preventDefault(); // 메뉴가 바로 사라지지 않도록 함
            menu.classList.toggle('show'); // 메뉴 열기
        }
    });
});