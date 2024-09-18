import Alpine from "alpinejs"

Alpine.data("edit_article", (isAuthenticated) => ({
    editing: false,
    articleContent: '',
    editContent: '',

    startEdit() {
        this.editing = true;
        this.articleContent  = this.$refs.articleContent.innerText;
    },

    cancelEdit() {
        this.editing = false;
    },

    saveEdit() {
        this.editing = false;
        this.$refs.articleContent.innerText = this.articleContent;
    },

    adjustHeight($el) {
        $el.style.height = 'auto';
        $el.style.height = $el.scrollHeight + 'px';
    },
}))


document.addEventListener('htmx:afterRequest', function(event) {
    if (event.detail.target.id === 'collect-button') {
        var button = document.getElementById('collect-button');

        // 假設服務器返回的是 HTML 片段，我們可以根據它來更新按鈕
        button.innerHTML = event.detail.xhr.responseText;

        // 如果你需要更具體的更新邏輯，可以根據返回內容進行處理
    }
});
