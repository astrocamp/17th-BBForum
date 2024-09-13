import Alpine from "alpinejs"

Alpine.data("optional_stock", (isAuthenticated) => ({
    isVisible: false,
    isAuthenticated: isAuthenticated,

    toggleVisibility(event) {
        event.stopPropagation(); // 阻止事件冒泡
        this.isVisible = !this.isVisible;
        console.log("11111111111111");
    },
}));