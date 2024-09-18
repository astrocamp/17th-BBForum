import Alpine from "alpinejs";

Alpine.data("unlogined_prompt", (isAuthenticated) => ({
    isVisible: false,
    isReadonly: false,
    isShow: false,
    isAuthenticated: isAuthenticated,
    articleContent: '',
    commentContent: '',
    tot_point: 0,
    current_user_groups:'',


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
        this.fetchAndUpdateLeftNavBar();
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
   
    async  fetchAndUpdateLeftNavBar() {
        try {
            const response = await fetch('http://127.0.0.1:8000/update-left-nav-bar/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (response.ok) {
                const data = await response.json();

                // 檢查是否有錯誤
                if (data.error) {
                    console.error('Error:', data.error);
                    return;
                }

                // 更新顯示
                const groupsDisplay = document.getElementById('groups_display');

                if (groupsDisplay) {
                    groupsDisplay.innerText = data.current_user_groups;
                }

            } else {
                console.error('Failed to fetch user groups');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }


}))

