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


    async fetchAndUpdateLeftNavBar() {
        try {
            const groupsDisplay = document.getElementById('groups_display');
            if (!groupsDisplay) {
                console.error('No element found for updating group display');
                return;
            }
            const response = await fetch('/update-left-nav-bar/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (response.ok) {
                const data = await response.json();

                if (data.error) {
                    console.error('Error:', data.error);
                    return;
                }
                const currentGroups = data.current_user_groups;
                if (groupsDisplay.innerText !== currentGroups) {
                    groupsDisplay.innerText = currentGroups;
                }
            } else {
                console.error('Failed to fetch user groups');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

}))

