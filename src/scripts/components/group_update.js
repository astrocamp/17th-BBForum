document.addEventListener('htmx:afterSwap', function(event) {
    // 如果發文成功，更新左側導航欄
    if (event.detail.target.id === 'articles_container') {
        fetchAndUpdateLeftNavBar();
    }
});