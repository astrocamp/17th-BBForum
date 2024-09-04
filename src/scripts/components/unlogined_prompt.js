import Alpine from "alpinejs"

Alpine.data("unlogined_prompt", (isAuthenticated) => ({
    isVisible: false,
    isReadonly: false,
    isShow: false,
    isAuthenticated: isAuthenticated,

    toggleVisibility() {
        this.isVisible = !this.isVisible;
        this.isReadonly = !this.isReadonly;
        this.isShow = !this.isShow;
    },

    submitForm() {
        const form = this.$el.closest("form")
        if (form) {
            form.addEventListener("submit", (e) => {
              e.preventDefault()
              form.submit()
            })
        }
        this.isVisible = !this.isVisible;
    }
}))