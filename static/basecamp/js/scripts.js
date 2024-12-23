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
    document.querySelectorAll('.nav-item.dropdown > .nav-link.dropdown-toggle').forEach(dropdownToggle => {
        dropdownToggle.addEventListener('click', function (e) {
            e.preventDefault(); // 기본 이벤트 방지
            e.stopPropagation(); // 이벤트 버블링 방지

            const dropdownMenu = this.nextElementSibling;

            // 모바일 화면에서만 작동
            if (window.innerWidth < 992) { // Bootstrap 'lg' breakpoint 이하
                // 현재 드롭다운 메뉴 토글
                if (dropdownMenu.classList.contains('show')) {
                    dropdownMenu.classList.remove('show');
                } else {
                    // 다른 드롭다운 메뉴 닫기
                    document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                        menu.classList.remove('show');
                    });
                    dropdownMenu.classList.add('show');
                }
            }
        });
    });

    // 🟢 외부 클릭 시 드롭다운 닫기
    window.addEventListener('click', function (e) {
        if (!e.target.closest('.nav-item.dropdown')) {
            document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                menu.classList.remove('show');
            });
        }
    });

    // 🟢 드롭다운 메뉴 항목 클릭 시 메뉴 닫기 (옵션)
    document.querySelectorAll('.dropdown-menu .dropdown-item').forEach(item => {
        item.addEventListener('click', function () {
            if (window.innerWidth < 992) {
                const dropdownMenu = this.closest('.dropdown-menu');
                dropdownMenu.classList.remove('show');
            }
        });
    });

});
