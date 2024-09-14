import Alpine from "alpinejs";

Alpine.data("unlogined_prompt", (isAuthenticated) => ({
    isVisible: false,
    isReadonly: false,
    isShow: false,
    isAuthenticated: isAuthenticated,
    articleContent: '',
    tot_point: 0,  // 用來顯示點數的初始值

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
        event.preventDefault();  // 防止默認表單提交行為
        console.log("Submitting form...");

        const formData = new FormData(this.$refs.submitForm);
        const response = await fetch(this.$refs.submitForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        if (response.ok) {
            const data = await response.json();

            if (data.success) {
                this.tot_point = data.tot_point;  // 更新點數
            } else {
                alert(data.error);
            }
        } else {
            console.error("提交文章失敗");
        }
    },

    // 用於提交評論的邏輯
    submitCommentForm(event) {
        if (this.commentContent.trim() === '') {
            event.preventDefault();
            alert("請輸入正確的留言訊息!!");
        } else {
            this.$refs.submitForm.requestSubmit();
            this.commentContent = '';
        }
    },

    // 獲取當前用戶點數的方法
    async fetchUserPoints() {
        const response = await fetch('/get-user-points/', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        if (response.ok) {
            const data = await response.json();
            this.tot_point = data.tot_point;  // 設置當前點數
        }
    }
}));
