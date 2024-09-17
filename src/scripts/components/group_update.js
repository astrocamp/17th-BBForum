
document.addEventListener('DOMContentLoaded', () => {
    fetch("http://127.0.0.1:8000/update-left-nav-bar/", {
        method: "GET",
        headers: {
            "hx-request": "true"
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('網絡錯誤：無法更新導航欄');
        }
        return response.text();
    })
    .then(html => {
        const navBar = document.querySelector("#left-nav-bar");
        if (navBar) {
            navBar.innerHTML = html;
        } else {
            console.error('找不到導航欄元素');
        }
        location.reload();
    })
    .catch(error => {
        console.error('更新導航欄時發生錯誤:', error);
    });
});