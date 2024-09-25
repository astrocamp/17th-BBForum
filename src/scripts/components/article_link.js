import Alpine from "alpinejs"

document.addEventListener('alpine:init', () => {


    Alpine.data('shareLinkComponent', () => ({
        showTooltip: false,
        copied: false,
        url: '',
        showLoginPrompt: false,
        init() {
            this.url = this.$el.getAttribute('data-url');
        },
        showTooltipBtn() {
            this.isAuthenticated ? (this.showTooltip = !this.showTooltip) : (this.showLoginPrompt = true);
        },
        copyLink() {
            navigator.clipboard.writeText(this.url)
                .then(() => {
                    this.copied = true;
                    setTimeout(() => {
                        this.copied = false;
                        this.showTooltip = false;
                    }, 1000);
                })
                .catch(() => {
                    console.error('無法複製連結');
                });
        }
    }));
});
