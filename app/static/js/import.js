function displayImportResult(result) {
  const resultContainer = document.getElementById("import-result");
  resultContainer.innerHTML = "";

  if (result.success) {
    const successAlert = document.createElement("div");
    successAlert.classList.add("alert", "alert-success");
    successAlert.textContent = "Data imported successfully!";
    resultContainer.appendChild(successAlert);
  } else {
    const errorAlert = document.createElement("div");
    errorAlert.classList.add("alert", "alert-danger");
    errorAlert.textContent = `Error importing data: ${result.error}`;
    resultContainer.appendChild(errorAlert);
  }
}

function handleImportForm(event) {
  event.preventDefault();

  const formData = new FormData(event.target);
  const fileInput = document.getElementById("file-input");
  const file = fileInput.files[0];

  if (!file) {
    displayImportResult({ success: false, error: "No file selected" });
    return;
  }

  const fileType = formData.get("file-type");
  formData.append("file", file, file.name);

  fetch("/import", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((result) => {
      displayImportResult(result);
      if (result.success) {
        window.location.href = `/import/result?result=${encodeURIComponent(
          JSON.stringify(result)
        )}`;
      }
    })
    .catch((error) => {
      console.error("Error importing data:", error);
      displayImportResult({
        success: false,
        error: "An error occurred during import",
      });
    });
}

const importForm = document.getElementById("import-form");
importForm.addEventListener("submit", handleImportForm);
