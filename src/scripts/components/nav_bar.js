import Alpine from "alpinejs";

document.addEventListener('alpine:init', () => {
    Alpine.data('nav_bar', () => ({
        showMenu: false,
        toggleMenu() {
            this.showMenu = !this.showMenu;
        }
    }));
});