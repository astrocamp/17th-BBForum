document.addEventListener('htmx:afterOnLoad', async function(event) {
    if (event.detail.target.id === 'articles_container') {
        try {

            const response = await fetch('/update-left-nav-bar/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (!response.ok) {
                console.error('Failed to fetch updated nav info');
                return;
            }

            const data = await response.json();

            if (data.error) {
                console.error('Error:', data.error);
                return;
            }

            const groupsDisplay = document.getElementById('groups_display');
            if (groupsDisplay) {
                groupsDisplay.innerText = data.current_user_groups;
            } else {
                console.error('Element #groups_display not found');
            }

        } catch (error) {
            console.error('Error:', error);
        }
    }
});


