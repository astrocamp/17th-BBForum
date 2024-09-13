import Alpine from "alpinejs"

document.addEventListener('alpine:init', () => {
    Alpine.data('toggleButtons', () => ({
        isButtonVisible: false,

        toggle() {
            this.isButtonVisible = !this.isButtonVisible;
        }
    }));
});
