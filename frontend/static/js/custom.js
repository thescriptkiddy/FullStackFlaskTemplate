function deleteItem(element, modelName) {
    const uuid = element.getAttribute('data-uuid');
    if (confirm('Are you sure you want to delete this item?')) {
        fetch(`/${modelName}/delete/${uuid}`, { method: 'DELETE' })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Redirect to the index page with a query parameter
                    window.location.href = `/${modelName}?message=` + encodeURIComponent(data.message) + '&category=success';
                } else {
                    // Show error message on the current page
                    showAlert(data.message, 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('An error occurred while deleting the item', 'danger');
            });
    }
}

function showAlert(message, category) {
    const alertContainer = document.getElementById('alert-container');
    const alertElement = document.createElement('div');
    alertElement.className = `alert alert-${category} alert-dismissible fade show`;
    alertElement.role = 'alert';
    alertElement.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    alertContainer.appendChild(alertElement);

    // Optional: Remove the alert after 5 seconds
    setTimeout(() => {
        alertElement.remove();
    }, 5000);
}


