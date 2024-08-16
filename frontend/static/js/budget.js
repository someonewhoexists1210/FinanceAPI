document.addEventListener('DOMContentLoaded', function() {
    const charts = {};
    document.querySelectorAll('.delete').forEach(function(button) {
        button.addEventListener('click', function() {
            const budgetId = this.dataset.id;
            fetch(`/delete-budget/${budgetId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.getElementById('csrf-token').value,
                },
            })
            .then(response => {
                if (response.ok) {
                    this.closest('tr').remove();
                    charts[budgetId].destroy();
                    document.getElementById(`chart-${budgetId}`).parentElement.remove();
                }
            });
        })
    });

    const budgets = JSON.parse(document.getElementById('budget-data').textContent);
    budgets.forEach(budget => {
        const ctx = document.getElementById(`chart-${budget.id}`).getContext('2d');
        charts[budget.id] = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Spent', 'Remaining'],
                datasets: [{
                    data: [budget.spent, budget.amount - budget.spent],
                    backgroundColor: ['#FF6384', '#36A2EB'],
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                }
            }
        });
    });
});