
const uploadButton = document.getElementById("upload-button");
const fileInput = document.getElementById("file-input");
const uploadedImage = document.getElementById("uploaded-image");
const results = document.getElementById("results");
const resultImage = document.getElementById("result-image");
const showResults = document.getElementById("show-results");
// set result path to empty image at first
let resultPath = ''


// Add a click event listener to the button
uploadButton.addEventListener("click", () => {
    // Trigger the file input click event when the button is clicked
    fileInput.click();
});

// Add an event listener to the file input
fileInput.addEventListener("change", () => {
    // Check if a file is selected
// show image in html page
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
    
    // send image to fastapi and get results
    if (file) {
        const formData = new FormData();
        formData.append("file", file);

        fetch("http://localhost:8000/process-image", {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response from the backend (e.g., display results)
            resultPath = data["output_path"]
            console.log(data);
        })
        .catch(error => {
            // Handle errors (e.g., display an error message)
            console.error(error);
        });
    }}
});


// // Add an event listener to the results: if it is clicked show results
// document.addEventListener('DOMContentLoaded', () => {

//     results.addEventListener("click", () => {
//             // Set the image source to the loaded file data URL
//             resultImage.src = resultPath;

//             // Display the uploaded image
//             resultImage.style.display = "block";
        
//     })});

document.body.addEventListener("click", (event) => {
    // Check if the clicked element has the ID "results"
    if (event.target.id === "results") {
        // Set the image source to the loaded file data URL
        resultImage.src = 'static/' + resultPath;
        // console.log(resultPath)

        // Display the uploaded image
        resultImage.style.display = "block";
    }
});