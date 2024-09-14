import Alpine from "alpinejs"

Alpine.data("optional_stock", (isAuthenticated) => ({
    isShow: false,
    isPick: false,
    checkstatus: false,
    isAuthenticated: isAuthenticated,

    init(checkPickURL) {
        this.checkPickStatus(checkPickURL);
    },

    async startPick(pickURL, unpickURL, checkPickURL, csrfToken) {
        this.isShow = !this.isShow;

        await this.checkPickStatus(checkPickURL);

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
            if (this.isPick) {
                this.$refs.buttonStyle.innerHTML = `
                <div class="w-[60px] h-[28px] rounded-[4px] bg-red-primary text-sm text-white flex items-center justify-center cursor-pointer border border-red-primary gap-1">
                    自選
                </div>`;
            } else {
                this.$refs.buttonStyle.innerHTML = `
                <div class="w-[60px] h-[28px] rounded-[4px] bg-white text-sm text-red-primary flex items-center justify-center cursor-pointer border border-red-primary gap-1">
                    自選
                </div>`;
            }

            this.isPick = !this.isPick;
        })
        .catch(error => {
            console.error('error:', error);
        });
    },

    async checkPickStatus(checkPickURL) {
        try {
            const response = await fetch(checkPickURL);
            const data = await response.json();

            if (data.is_picked) {
                this.isPick = true;
            } else {
                this.isPick = false;
            }

            if (this.isPick) {
                this.$refs.buttonStyle.innerHTML = `
                <div class="w-[60px] h-[28px] rounded-[4px] bg-white text-sm text-red-primary flex items-center justify-center cursor-pointer border border-red-primary gap-1">
                    自選
                </div>`;
            } else {
                console.log(this.$refs.buttonStyle)
                this.$refs.buttonStyle.innerHTML = `
                <div class="w-[60px] h-[28px] rounded-[4px] bg-red-primary text-sm text-white flex items-center justify-center cursor-pointer border border-red-primary gap-1">
                    自選
                </div>`;
            }
        } catch (error) {
            console.error('error:', error);
        }
    }
}));