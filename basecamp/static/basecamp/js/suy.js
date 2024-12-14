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

// Function to hide the notice box and open the link
function hideNoticeBox(event, link, target) {
    event.preventDefault(); // Prevent default link behavior
    const noticeBox = document.querySelector('.notice-box-link');
    if (noticeBox) {
        noticeBox.style.display = 'none'; // Hide the notice box
    }
    // Open the link in the appropriate target
    if (target === "_blank") {
        window.open(link, target);
    } else {
        window.location.href = link; // Navigate to the link in the same window
    }
}
// Function to hide the notice box when the close button is clicked
function closeNoticeBox(event) {
    event.preventDefault(); // Prevent the default link behavior temporarily
        const noticeBox = document.querySelector('.notice-box-link');
        if (noticeBox) {
            noticeBox.style.display = 'none'; // Hide the notice box
        }
        // Allow the link to open after hiding the notice box
        setTimeout(() => {
            window.open(event.currentTarget.href, event.currentTarget.target);
        }, 0);
    }