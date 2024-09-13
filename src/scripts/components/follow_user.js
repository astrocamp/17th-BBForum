import Alpine from "alpinejs"

Alpine.data("follow_user", (isAuthenticated, articleUserId, currentUserId) => ({
    isVisible: false,
    isShow: false,
    isFollow: false,
    checkstatus: false,
    hasChecked: false,
    isAuthenticated: isAuthenticated,
    isOwnPost: articleUserId === currentUserId,

    async followUser(followURL, unfollowURL, checkFollowURL, csrfToken) {
        this.isShow = !this.isShow;

        await this.checkFollowStatus(checkFollowURL);

        const url = this.isFollow ? unfollowURL : followURL;
        const method = this.isFollow ? 'DELETE' : 'POST';

        fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({}),
        })
        .then(response => response.json())
        .then(data => {
            console.log(this.isFollow)

            if (this.isFollow) {
                this.$refs.buttonStyle.style.background = '#ae2024';
                this.$refs.buttonStyle.textContent = '追蹤';
                this.$refs.buttonStyle.style.color = 'white';
            } else {
                this.$refs.buttonStyle.style.background = '#0066CC';
                this.$refs.buttonStyle.textContent = '取消追蹤';
                this.$refs.buttonStyle.style.color = 'white';
            }

            this.isFollow = !this.isFollow;
        })
        .catch(error => {
            console.error('error:', error);
        });
    },

    async chackMouseoverColor(checkFollowURL) {
        this.isShow = true

        if (!this.hasChecked) {
            await this.checkFollowStatus(checkFollowURL);

            if (this.isFollow) {
                this.$refs.buttonStyle.style.background = '#3d6aaf';
                this.$refs.buttonStyle.textContent = '取消追蹤';
                this.$refs.buttonStyle.style.color = 'white';
            } else {
                this.$refs.buttonStyle.style.background = '#ae2024';
                this.$refs.buttonStyle.textContent = '追蹤';
                this.$refs.buttonStyle.style.color = 'white';
            }
            this.hasChecked = true;
        }
    },

    async checkFollowStatus(checkFollowURL) {
        try {
            const response = await fetch(checkFollowURL);
            const data = await response.json();

            if (data.is_following) {
                this.isFollow = true;
            } else {
                this.isFollow = false;
            }
        } catch (error) {
            console.error('error:', error);
        }
    }
}));

