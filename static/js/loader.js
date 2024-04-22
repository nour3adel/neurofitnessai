// Function to show the loader
function showLoader() {
    document.querySelector('.loader-container').style.display = 'flex';
    document.querySelector('.content').style.display = 'none';
  }
  
  // Function to hide the loader
  function hideLoader() {
    document.querySelector('.loader-container').style.display = 'none';
    document.querySelector('.content').style.display = 'block';
  }
  
  // Simulate a delay for demonstration purposes
  setTimeout(hideLoader, 1500); // Adjust the delay time as needed
  