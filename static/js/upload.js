document.addEventListener("DOMContentLoaded", () => {
  const uploadForm = document.getElementById("uploadForm");
  const uploadMessage = document.getElementById("uploadMessage");
  const loadingOverlay = document.getElementById("loadingOverlay");

  const uploadImageDisplay = document.getElementById("upload-image");
  const inputImage = document.getElementById("imageFile");

  inputImage.onchange = () => {
    uploadImageDisplay.src = URL.createObjectURL(inputImage.files[0]);
  };

  const csrfToken = document.querySelector(
    'input[name="csrfmiddlewaretoken"]'
  ).value;

  uploadForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    loadingOverlay.style.display = "flex";

    const formData = new FormData(uploadForm);

    try {
      const response = await fetch("/api/upload", {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
        },
        body: formData,
      });

      const result = await response.json();

      if (response.ok) {
        uploadMessage.textContent = result.message;
        uploadMessage.style.color = "green";
        uploadForm.reset();
      } else {
        throw new Error(result.error || "Upload failed");
      }
    } catch (error) {
      uploadMessage.textContent = error.message;
      uploadMessage.style.color = "red";
    } finally {
      loadingOverlay.style.display = "none";
    }
  });
});
