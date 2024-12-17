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
            // 먼저 배경 이미지를 변경하기 전에 opacity를 0으로 설정하여 사라지게 함
            header.style.transition = "opacity 2s ease-in-out"; // 트랜지션 추가
            header.style.opacity = 0;  // 이미지가 사라지도록 설정

            // setTimeout을 사용하여 opacity를 0으로 만든 후 새로운 이미지 적용
            setTimeout(function() {
                header.style.backgroundImage = `url(${images[currentIndex]})`; 
                // opacity를 1로 변경하여 부드럽게 나타나도록 설정
                header.style.opacity = 1;
            }, 2000); // 2초 동안 opacity가 0이 되게 한 후, 이미지 변경

            currentIndex = (currentIndex + 1) % images.length; // 이미지 인덱스 순환
        }
    }      

    setInterval(changeBackgroundImage, 5000);  // 5초 간격으로 배경 이미지 변경
});
