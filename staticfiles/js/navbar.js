document.addEventListener("DOMContentLoaded", function() {
    const navbarToggler = document.querySelector(".navbar-toggler"); // Navbar açma butonu
    const navbarCollapse = document.querySelector(".navbar-collapse"); // Açılır menü
    const coffeImage = document.querySelector(".coffe_image_group"); // Resim grubu

    navbarToggler.addEventListener("click", function() {
        setTimeout(() => {
            if (navbarCollapse.classList.contains("show")) {
                coffeImage.style.top = "250px"; // Navbar açılınca aşağı kaydır
            } else {
                coffeImage.style.top = "100px"; // Navbar kapanınca eski yerine getir
            }
        }, 300); // Animasyonun oturması için küçük bir gecikme ekledik
    });
});
