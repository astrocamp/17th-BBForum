import Alpine from "alpinejs"

Alpine.data("edit_comment", (isAuthenticated) => ({
    editing: false,
    commentContent: '',
    editContent: '',

    startEdit() {
        this.editing = true;
        this.commentContent  = this.$refs.commentContent.innerText;
    },

    cancelEdit() {
        this.editing = false;
    },

    saveEdit() {
        this.editing = false;
    },

    adjustHeight($el) {
        $el.style.height = '100%';
        $el.style.height = $el.scrollHeight + 'px';
    },
}))