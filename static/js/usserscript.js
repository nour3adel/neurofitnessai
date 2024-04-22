
function loadPage(page) {
    // Fetch content from the specified page
    fetch(page)
        .then(response => response.text())
        .then(html => {
            // Replace content with the loaded HTML
            document.getElementById('content').innerHTML = html;
        })
        .catch(error => console.error(`Error fetching ${page}:`, error));
}

