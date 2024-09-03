import Alpine from "alpinejs"

Alpine.data("switch_page", (isAuthenticated) => ({
    isVisible: false,
    isReadonly: false,
    isShow: false,
    isAuthenticated: isAuthenticated,

    toggleVisibility() {
        this.isVisible = !this.isVisible;
        this.isReadonly = !this.isReadonly;
        this.isShow = !this.isShow;
    },

    navigatePage(pages_url) {
        this.isAuthenticated ? window.location.href = pages_url : this.toggleVisibility()
    }
}))