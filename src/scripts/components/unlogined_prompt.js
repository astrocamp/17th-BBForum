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

    async submitArticleForm(event) {
        event.preventDefault();

        const formData = new FormData(this.$refs.submitForm);
        const response = await fetch(this.$refs.submitForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        const data = await response.json();
        console.log(data);
        if (data.success) {
            document.getElementById('points-display').innerText = `P點: ${data.tot_point}`;
            this.articleContent = '';
            this.$refs.clearTextarea.value = '';
        } else {
            console.error(data.error);
        }
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
}));