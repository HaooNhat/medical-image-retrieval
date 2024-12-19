document.addEventListener("DOMContentLoaded", () => {
  const queryImage = document.getElementById("query-image");
  const inputImage = document.getElementById("inputQueryImage");
  const resultsContainer = document.getElementById("resultsContainer");
  const sidebar = document.getElementById("sidebar");
  const imageDetails = document.getElementById("imageDetails");
  const closeSidebarButton = document.getElementById("closeSidebar");
  const queryCompareImage = document.getElementById("queryImage");
  const selectedImage = document.getElementById("selectedImage");

  inputImage.onchange = () => {
    queryImage.src = URL.createObjectURL(inputImage.files[0]);
    queryCompareImage.src = queryImage.src;
  };

  const submitForm = document.getElementById("submitForm");
  const csrfToken = document.querySelector(
    'input[name="csrfmiddlewaretoken"]'
  ).value;
  const errorMessage = document.getElementById("error-message");

  errorMessage.style.opacity = 0;

  submitForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("query_image", inputImage.files[0]);

    fetch("/api/query", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        // console.log("Client: " + data)
        displayResults(data["results"]);
      })
      .catch((error) => {
        console.error(error);
      });
  });

  function displayResults(results) {
    document
      .getElementsByClassName("results-section")[0]
      .classList.add("active");
    resultsContainer.innerHTML = "";
    results.forEach((result, idx) => {
      const resultItem = document.createElement("div");
      resultItem.className = "result-item";
      resultItem.innerHTML = `
    <p>${idx + 1}</p>
                <img src="${result.image_url}" alt="${
        result.image_filename
      }" class="result-image">
            `;
      resultItem.addEventListener("click", () => showDetails(result));
      resultsContainer.appendChild(resultItem);
      resultsContainer.style.marginTop = "20px";
    });
  }

  function showDetails(result) {
    document.getElementById("comparison-image").classList.add("active");
    selectedImage.src = `${result.image_url}`;
    imageDetails.innerHTML = `
            <h3>${result.image_filename}</h3>
            <p>Labels: ${result.labels}</p>
            <p>Patient ID: ${result.patient_id}</p>
            <p>Age: ${result.patient_age}</p>
            <p>Gender: ${result.patient_gender}</p>
            <p>View Position: ${result.view_position}</p>
        `;
    sidebar.classList.add("active");
  }

  function closeSidebar() {
    sidebar.classList.remove("active");
    document.getElementById("comparison-image").classList.remove("active");
  }

  closeSidebarButton.addEventListener("click", closeSidebar);

  // Close sidebar when clicking outside
  document.addEventListener("click", (e) => {
    if (!sidebar.contains(e.target) && !e.target.closest(".result-item")) {
      closeSidebar();
    }
  });
});
