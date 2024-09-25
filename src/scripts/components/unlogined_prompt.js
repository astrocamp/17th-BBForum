import Alpine from "alpinejs";

Alpine.data("unlogined_prompt", (isAuthenticated) => ({
    isVisible: false,
    isReadonly: false,
    isShow: false,
    isAuthenticated: isAuthenticated,
    articleContent: '',
    commentContent: '',
    tot_point: 0,

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
        this.fetchUserPoints();
    },

    submitCommentForm(event) {
        if (this.commentContent.trim() === '') {
            event.preventDefault();
            alert("請輸入正確的留言訊息!!");
        } else {
            this.$refs.submitForm.requestSubmit();
            this.commentContent = '';
        }
    },

    submitForcus(id) {
        this.isVisible = !this.isVisible;
        this.isReadonly = !this.isReadonly;
        this.isShow = !this.isShow;

        if (isAuthenticated) {
            this.$dispatch('focus-textarea', { id: id });
        }
    },

    async fetchUserPoints() {
        const response = await fetch('/points/get-user-points/', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        if (response.ok) {
            const data = await response.json();
            this.tot_point = data.tot_point;
            document.getElementById('points-display').innerText = `P點: ${this.tot_point}`;
        }
    },
}));
