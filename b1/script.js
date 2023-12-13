function searchPhotos() {
  const query = document.getElementById('query').value;

  // Use the SDK to make a GET request to the /search endpoint
  sdk.search({ q: query })
    .then(response => {
      // Handle the response and display results
      displayResults(response);
    })
    .catch(error => {
      console.error('Error:', error);
      // Handle errors gracefully
    });
}

function displayResults(results) {
  const resultsDiv = document.getElementById('results');
  resultsDiv.innerHTML = '';

  if (results.length === 0) {
    resultsDiv.innerHTML = 'No results found.';
  } else {
    results.forEach(result => {
      // Customize the display of each result as needed
      const resultItem = document.createElement('div');
      resultItem.textContent = result.objectKey; // Adjust based on your API response
      resultsDiv.appendChild(resultItem);
    });
  }
}


function uploadPhoto() {
    const fileInput = document.getElementById('photo');
    const customLabelsInput = document.getElementById('customLabels');

    const file = fileInput.files[0];
    const customLabels = customLabelsInput.value.split(',');

    // Use the SDK to make a PUT request to the /photos endpoint with custom headers
    const customHeaders = {
      'x-amz-meta-customLabels': customLabels.join(',')
    };

    sdk.upload(file, customHeaders)
      .then(response => {
        // Handle the response and display the result
        displayUploadResult(response);
      })
      .catch(error => {
        console.error('Error:', error);
        // Handle errors gracefully
      });
}

function displayUploadResult(response) {
const uploadResultDiv = document.getElementById('uploadResult');
uploadResultDiv.innerHTML = '';

if (response.statusCode === 200) {
    uploadResultDiv.innerHTML = 'Photo uploaded successfully.';
} else {
    uploadResultDiv.innerHTML = `Error: ${response.body}`;
}
}
