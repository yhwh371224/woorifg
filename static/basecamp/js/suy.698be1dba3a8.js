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


// Check if the notice has already been clicked
document.addEventListener("DOMContentLoaded", function () {
    if (localStorage.getItem("noticeSeen") === "true") {
        const noticeBox = document.querySelector('.notice-box-link');
        if (noticeBox) {
            noticeBox.style.display = 'none';
        }
    }
});

// Function to hide the notice box and mark it as seen
function hideNoticeBox() {
    localStorage.setItem("noticeSeen", "true");
}
