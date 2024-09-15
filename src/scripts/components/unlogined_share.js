import Alpine from "alpinejs"

Alpine.data("unlogined_share", (isAuthenticated) => ({
    isVisible: false,
    isReadonly: false,
    isShow: false,
    isAuthenticated: isAuthenticated,
    articleContent: '',
    commentContent: '',
    showPublishArticle: false,
    showNotLogged: false,

    toggleVisibility() {
        this.isVisible = !this.isVisible;
    },

    submitForm() {
        if (this.$refs.clearTextarea) {
            this.$refs.clearTextarea.value = '';
        }
        this.isVisible = !this.isVisible;
    },

    submitCommentForm(event) {
        if(this.commentContent.trim() === '') {
            event.preventDefault();
            alert("請輸入正確的留言訊息!!");
        } else {
            this.$refs.submitForm.requestSubmit();
            this.commentContent = '';
        }
    },
}))