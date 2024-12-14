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
        results = [
          {
            image_filename: "00000017_001.png",
            labels: "No Finding",
            patient_id: "00000017",
            patient_age: 77,
            patient_gender: "M",
            view_position: "AP",
            id: 454289029618204676,
          },
          {
            image_filename: "00009229_020.png",
            labels: "No Finding",
            patient_id: "00009229",
            patient_age: 37,
            patient_gender: "M",
            view_position: "AP",
            id: 454289084503821730,
          },
          {
            image_filename: "00019981_002.png",
            labels: "No Finding",
            patient_id: "00019981",
            patient_age: 40,
            patient_gender: "F",
            view_position: "AP",
            id: 454289156542308270,
          },
          {
            image_filename: "00005682_006.png",
            labels: "Edema",
            patient_id: "00005682",
            patient_age: 74,
            patient_gender: "M",
            view_position: "AP",
            id: 454289063535183984,
          },
          {
            image_filename: "00007131_000.png",
            labels: "No Finding",
            patient_id: "00007131",
            patient_age: 57,
            patient_gender: "M",
            view_position: "AP",
            id: 454289072897133246,
          },
          {
            image_filename: "00007121_003.png",
            labels: "No Finding",
            patient_id: "00007121",
            patient_age: 62,
            patient_gender: "F",
            view_position: "AP",
            id: 454289072801974968,
          },
          {
            image_filename: "00016942_000.png",
            labels: "No Finding",
            patient_id: "00016942",
            patient_age: 58,
            patient_gender: "M",
            view_position: "AP",
            id: 454289137322695380,
          },
          {
            image_filename: "00019594_003.png",
            labels: "Effusion",
            patient_id: "00019594",
            patient_age: 56,
            patient_gender: "M",
            view_position: "AP",
            id: 454289153915363074,
          },
          {
            image_filename: "00018175_006.png",
            labels: "No Finding",
            patient_id: "00018175",
            patient_age: 56,
            patient_gender: "M",
            view_position: "AP",
            id: 454289145653370090,
          },
          {
            image_filename: "00004746_018.png",
            labels: "No Finding",
            patient_id: "00004746",
            patient_age: 41,
            patient_gender: "F",
            view_position: "AP",
            id: 454289057658963706,
          },
          {
            image_filename: "00016787_003.png",
            labels: "No Finding",
            patient_id: "00016787",
            patient_age: 51,
            patient_gender: "M",
            view_position: "AP",
            id: 454289136478591646,
          },
          {
            image_filename: "00012681_049.png",
            labels: "No Finding",
            patient_id: "00012681",
            patient_age: 60,
            patient_gender: "F",
            view_position: "AP",
            id: 454289109020578748,
          },
          {
            image_filename: "00005202_000.png",
            labels: "No Finding",
            patient_id: "00005202",
            patient_age: 56,
            patient_gender: "F",
            view_position: "AP",
            id: 454289060803905474,
          },
          {
            image_filename: "00029016_000.png",
            labels: "No Finding",
            patient_id: "00029016",
            patient_age: 72,
            patient_gender: "M",
            view_position: "PA",
            id: 454289199148050940,
          },
          {
            image_filename: "00004090_002.png",
            labels: "Edema",
            patient_id: "00004090",
            patient_age: 61,
            patient_gender: "M",
            view_position: "AP",
            id: 454289054191322652,
          },
          {
            image_filename: "00007526_034.png",
            labels: "No Finding",
            patient_id: "00007526",
            patient_age: 66,
            patient_gender: "M",
            view_position: "AP",
            id: 454289075310693208,
          },
          {
            image_filename: "00003482_001.png",
            labels: "No Finding",
            patient_id: "00003482",
            patient_age: 75,
            patient_gender: "F",
            view_position: "AP",
            id: 454289050640581954,
          },
          {
            image_filename: "00014116_006.png",
            labels: "Atelectasis|Infiltration",
            patient_id: "00014116",
            patient_age: 54,
            patient_gender: "M",
            view_position: "AP",
            id: 454289118933030456,
          },
          {
            image_filename: "00023033_002.png",
            labels: "Nodule",
            patient_id: "00023033",
            patient_age: 63,
            patient_gender: "M",
            view_position: "AP",
            id: 454289173949719548,
          },
          {
            image_filename: "00007406_003.png",
            labels: "No Finding",
            patient_id: "00007406",
            patient_age: 66,
            patient_gender: "M",
            view_position: "AP",
            id: 454289074501716772,
          },
        ];
        displayResults(results);
      })
      .catch((error) => {
        console.error(error);
      });
  });

  function displayResults(results) {
    resultsContainer.innerHTML = "";
    results.forEach((result, idx) => {
      const resultItem = document.createElement("div");
      resultItem.className = "result-item";
      resultItem.innerHTML = `
    <p>${idx + 1}</p>
                <img src="/static/image/${result.image_filename}" alt="${
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
    selectedImage.src = `static/image/${result.image_filename}`;
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
