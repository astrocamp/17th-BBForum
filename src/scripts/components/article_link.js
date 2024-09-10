import Alpine from "alpinejs"

Alpine.data('shareLinkComponent', () => ({
    showTooltip: false,
    copied: false,
    url: '',

    init() {
        // 從 data-url 屬性中讀取 URL
        const urlElement = this.$el.dataset.url;
        if (urlElement) {
            this.url = urlElement;
            console.log('Article URL:', this.url);
        } else {
            console.error('未找到 URL');
        }
    },

    copyLink() {
        navigator.clipboard.writeText(this.url)
            .then(() => {
                this.copied = true;
                setTimeout(() => this.copied = false, 2000);
            })
            .catch(err => console.error('複製失敗', err));
    }
}));

Alpine.start();