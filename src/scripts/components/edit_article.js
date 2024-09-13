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
    },
}))


