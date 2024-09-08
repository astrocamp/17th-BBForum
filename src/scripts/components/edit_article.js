import Alpine from "alpinejs"

Alpine.data("edit_article", (isAuthenticated) => ({
    editing: false,
    articleContent: '',
    editContent: '',

    startEdit() {
        this.editing = true;
        this.articleContent  = this.$refs.articleContent.innerText;
    },

    cancelEdit() {
        this.editing = false;
    },

    saveEdit() {
        this.editing = false;
        this.$refs.articleContent.innerText = this.articleContent;
    },

    adjustHeight($el) {
        $el.style.height = 'auto';
        $el.style.height = $el.scrollHeight + 'px';
        // this.$refs.containerDiv.style.height = 'auto'; // 確保外層 div 高度自適應
        // this.$refs.containerDiv.style.height = $el.scrollHeight + 'px'; // 同步外層 div 高度
    },
}))