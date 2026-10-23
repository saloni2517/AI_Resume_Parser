const resumeInput = document.getElementById("resume");
const fileNameDisplay = document.getElementById("file-name");

if (resumeInput && fileNameDisplay) {
    resumeInput.addEventListener("change", function () {
        const file = this.files[0];

        if (!file) {
            fileNameDisplay.textContent = "No file selected";
            return;
        }

        const allowedExtensions = [".pdf", ".docx"];
        const fileName = file.name.toLowerCase();

        const isAllowed = allowedExtensions.some(extension =>
            fileName.endsWith(extension)
        );

        if (!isAllowed) {
            fileNameDisplay.textContent =
                "Please select a PDF or DOCX file.";

            this.value = "";
            return;
        }

        const maxSize = 5 * 1024 * 1024;

        if (file.size > maxSize) {
            fileNameDisplay.textContent =
                "File is too large. Maximum size is 5 MB.";

            this.value = "";
            return;
        }

        fileNameDisplay.textContent = "Selected: " + file.name;
    });
}