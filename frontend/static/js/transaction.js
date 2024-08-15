document.addEventListener('DOMContentLoaded', function() {
const csrfToken = document.getElementById('csrf-token').value;
document.querySelectorAll('.delete').forEach(function(button) {
    console.log('button', button);
    button.addEventListener('click', function() {
        const transactionId = this.dataset.id;
        fetch(`/delete-transaction/${transactionId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
        })
        .then(response => {
            if (response.ok) {
                this.closest('tr').remove();
            }
        });
    });
});
});
