document.addEventListener('DOMContentLoaded', function () {

    // 🟢 Navbar Shrink 기능
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) return;

        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink');
        } else {
            navbarCollapsible.classList.add('navbar-shrink');
        }
    };

    navbarShrink();
    document.addEventListener('scroll', navbarShrink);

    // 🟢 ScrollSpy 활성화
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    }

    // 🟢 Navbar Toggler 클릭 이벤트
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );

    responsiveNavItems.forEach(responsiveNavItem => {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

    // 🟢 드롭다운 메뉴 이벤트 핸들링
    document.querySelectorAll('.dropdown').forEach(dropdown => {
        const menu = dropdown.querySelector('.dropdown-menu');

        // 📱 모바일 드롭다운 (화면 너비 768px 이하)
        dropdown.addEventListener('click', function (e) {
            if (window.innerWidth < 768) {
                e.stopPropagation(); // 이벤트 전파 중단
                menu.classList.toggle('show');
            }
        });

        // 🖥️ 데스크톱 드롭다운 (화면 너비 768px 이상)
        dropdown.addEventListener('mouseenter', function () {
            if (window.innerWidth >= 768) {
                menu.classList.add('show');
            }
        });

        dropdown.addEventListener('mouseleave', function () {
            if (window.innerWidth >= 768) {
                menu.classList.remove('show');
            }
        });

        // 메뉴 항목 클릭 시 닫히지 않도록 설정 (모바일)
        menu.querySelectorAll('.dropdown-item').forEach(item => {
            item.addEventListener('click', function (e) {
                e.stopPropagation(); // 이벤트 전파 중단
            });
        });
    });

    // 🟢 드롭다운 외부 클릭 시 닫기
    window.addEventListener('click', function (e) {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                menu.classList.remove('show');
            });
        }
    });

});
