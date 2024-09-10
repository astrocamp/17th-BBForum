import Alpine from "alpinejs"

Alpine.data("unlogined_prompt", (isAuthenticated) => ({
    isVisible: false,
    isReadonly: false,
    isShow: false,
    isAuthenticated: isAuthenticated,
    articleContent: '',
    commentContent: '',

    toggleVisibility() {
        this.isVisible = !this.isVisible;
        this.isReadonly = !this.isReadonly;
        this.isShow = !this.isShow;
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

    checkAndSubmit(event) {
        if (this.articleContent.trim() === '') {
            event.preventDefault();
            alert('請輸入正確的留言訊息!!');
            return;
        } else {
            this.$refs.submitArticleForm.requestSubmit();
            this.articleContent = '';
        }
    }
}))