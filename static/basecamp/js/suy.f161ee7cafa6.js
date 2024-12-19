// 이미지 슬라이더 코드
document.addEventListener('DOMContentLoaded', function () {
    const slides = document.querySelectorAll('.image-slider .slide');
    let currentIndex = 0;

    function changeSlide() {
        // 현재 슬라이드 비활성화
        slides[currentIndex].classList.remove('active');

        // 다음 슬라이드 활성화
        currentIndex = (currentIndex + 1) % slides.length;
        slides[currentIndex].classList.add('active');
    }

    // 5초마다 슬라이드 변경
    setInterval(changeSlide, 5000);
});

