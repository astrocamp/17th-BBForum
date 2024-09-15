import Alpine from "alpinejs"

document.addEventListener('alpine:init', () => {
    Alpine.data('fileUploader', () => ({
        fileName: '',
        filePreview: '',

        previewFile(event) {
            const file = event.target.files[0];
            if (file) {
                this.fileName = file.name;
                const reader = new FileReader();
                reader.onload = (e) => {
                    this.filePreview = e.target.result;
                };
                reader.readAsDataURL(file);
            } else {
                this.fileName = '';
                this.filePreview = '';
            }
        }
    }));
});