
const uploadButton = document.getElementById("upload-button");
const fileInput = document.getElementById("file-input");
const uploadedImage = document.getElementById("uploaded-image");

// Add a click event listener to the button
uploadButton.addEventListener("click", () => {
    // Trigger the file input click event when the button is clicked
    fileInput.click();
});

// Add an event listener to the file input
fileInput.addEventListener("change", () => {
    // Check if a file is selected
    if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        // console.log(fileInput.files)
        // Create a FileReader to read the selected file
        const reader = new FileReader();

        // Define what to do when the file is loaded
        reader.onload = (e) => {
            // Set the image source to the loaded file data URL
            uploadedImage.src = e.target.result;

            // Display the uploaded image
            uploadedImage.style.display = "block";
        };
        console.log(file)
        // Read the selected file as a data URL (image)
        reader.readAsDataURL(file);
    }
});