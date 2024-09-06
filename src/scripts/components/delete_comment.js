import Alpine from "alpinejs"

Alpine.data("delete_comment", (isAuhenticated) => ({

    deleteComment() {
        if (isAuhenticated) {
            this.$el.closest('div.comment').remove()
        }
    },
}))