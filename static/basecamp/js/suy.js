document.addEventListener("DOMContentLoaded", function() {
    const baseUrl = "/static/basecamp/assets/img/"; // 기본 경로를 설정

    const images = [
        baseUrl + "suy7.webp",
        baseUrl + "suy8.webp",
        baseUrl + "suy5.webp"
    ];    

    let currentIndex = 0;

    function changeBackgroundImage() {
        const header = document.querySelector('header.masthead');
        if (header) {
            const imgUrl = images[currentIndex];
            const img = new Image();
            img.src = imgUrl;

            // 이미지가 성공적으로 로드된 후 배경 이미지 변경
            img.onload = function() {
                // 새로운 배경 이미지 로드 전에 기존 배경 이미지를 유지
                header.style.opacity = 0;  // 기존 배경을 숨김
                header.style.backgroundImage = `url(${imgUrl})`;  // 새로운 이미지 설정

                // 이미지 로드 후 opacity를 1로 설정하여 부드럽게 전환
                setTimeout(function() {
                    header.style.opacity = 1;
                }, 100); // 약간의 지연을 줘서 전환 효과가 자연스러워짐
            };

            // 인덱스를 변경하여 다음 이미지로 넘어가도록 설정
            currentIndex = (currentIndex + 1) % images.length;
        }
    }

    // 3초마다 배경 이미지 변경
    setInterval(changeBackgroundImage, 3000);
});
