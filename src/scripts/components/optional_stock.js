import Alpine from "alpinejs"

Alpine.data("optional_stock", (isAuthenticated) => ({
    isShow: false,
    isPick: false,
    checkstatus: false,
    isAuthenticated: isAuthenticated,
    // isOwnPost: pickUserId === currentStockId,

    async startPick(pickURL, unpickURL, checkPickURL, csrfToken) {
        this.isShow = !this.isShow;

        // await this.checkFollowStatus(checkPickURL);
        console.log("-----------------------------")
        console.log(pickURL)
        console.log(unpickURL)
        console.log(checkPickURL)
        console.log(csrfToken)

        const url = this.isPick ? unpickURL : pickURL;
        const method = this.isPick ? 'DELETE' : 'POST';

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
            console.log(this.isPick)

            // if (this.isPick) {
            //     this.$refs.buttonStyle.style.background = '#ae2024';
            //     this.$refs.buttonStyle.textContent = '追蹤';
            //     this.$refs.buttonStyle.style.color = 'white';
            // } else {
            //     this.$refs.buttonStyle.style.background = '#0066CC';
            //     this.$refs.buttonStyle.textContent = '取消追蹤';
            //     this.$refs.buttonStyle.style.color = 'white';
            // }

            this.isPick = !this.isPick;
        })
        .catch(error => {
            console.error('error:', error);
        });
    },

    async checkPickStatus(checkFollowURL) {
        try {
            const response = await fetch(checkFollowURL);
            const data = await response.json();

            if (data.is_following) {
                this.isPick = true;
            } else {
                this.isPick = false;
            }
        } catch (error) {
            console.error('error:', error);
        }
    }
}));