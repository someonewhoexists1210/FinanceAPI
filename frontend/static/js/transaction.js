document.addEventListener('DOMContentLoaded', function() {
    let title = document.getElementById('title');
    let from = document.getElementById('balance-from');
    let to = document.getElementById('balance-to');
    let csrfToken = document.getElementById('csrf-token').value;

    let options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({amount: 100}),
    }

    fetch('/back/balance').then(response => response.json())
    .then(data => from.innerHTML = data.balance + ' € =>');
    fetch('/back/transaction/', options).then(response => {
        if (response.status === 200) {
            title.innerHTML = 'Transaction Successful';
            response.json().then(data => to.innerHTML = data.balance + ' €');
        } else {
            title.innerHTML = 'Transaction Failed';
            to.innerHTML = 'Error';
            from.innerHTML = '';
        }
    })
});