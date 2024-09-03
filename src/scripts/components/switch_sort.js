import Alpine from "alpinejs"

Alpine.data("switch_sort", (isAuthenticated) => ({
    isVisible: false,

    toggleVisibility() {
        this.isVisible = !this.isVisible;
    },
}))