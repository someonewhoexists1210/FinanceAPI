document.addEventListener('DOMContentLoaded', function() {
    console.log(document.getElementById('budget_data').value)
    const budgetData = JSON.parse(document.getElementById('budget_data').value);

    const labels = budgetData.map(budget => budget.goal_name);
    const data = budgetData.map(budget => parseFloat(budget.amount));

    const ctx = document.getElementById('budgetChart').getContext('2d');
    const budgetChart = new Chart(ctx, {
        type: 'bar', 
        data: {
            labels: labels,
            datasets: [{
                label: 'Budget Amounts',
                data: data,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
