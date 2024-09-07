document.addEventListener('DOMContentLoaded', function () {
    const incomeForm = document.getElementById('add-income-form');
    const expenseForm = document.getElementById('add-expense-form');

    const incomePieCtx = document.getElementById('incomePieChart').getContext('2d');
    const expensePieCtx = document.getElementById('expensePieChart').getContext('2d');

    let incomePieChart = createPieChart(incomePieCtx, 'Income Distribution');
    let expensePieChart = createPieChart(expensePieCtx, 'Expense Distribution');

    function createPieChart(ctx, label) {
        return new Chart(ctx, {
            type: 'pie',
            data: {
                labels: [],
                datasets: [{
                    label: label,
                    data: [],
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.6)',
                        'rgba(54, 162, 235, 0.6)',
                        'rgba(255, 206, 86, 0.6)',
                        'rgba(75, 192, 192, 0.6)',
                        'rgba(153, 102, 255, 0.6)'
                    ],
                    borderColor: 'rgba(255, 255, 255, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    }
                }
            }
        });
    }

    function updatePieChart(chart, labels, values) {
        chart.data.labels = labels;
        chart.data.datasets[0].data = values;
        chart.update();
    }

    function appendTransactionToTable(tableBody, amount, category, date) {
        const row = tableBody.insertRow();
        row.insertCell(0).textContent = amount;
        row.insertCell(1).textContent = category;
        row.insertCell(2).textContent = date;
    }

    function handleFormSubmit(form, chart, tableBody, isIncome = true) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            const amount = form.querySelector('input[type="number"]').value;
            const category = form.querySelector('input[type="text"]').value;
            const date = new Date().toLocaleString();

            if (!amount || !category) {
                alert('Please fill in all fields.');
                return;
            }

            appendTransactionToTable(tableBody, amount, category, date);

            const chartDataIndex = chart.data.labels.indexOf(category);
            if (chartDataIndex >= 0) {
                chart.data.datasets[0].data[chartDataIndex] += parseFloat(amount);
            } else {
                chart.data.labels.push(category);
                chart.data.datasets[0].data.push(parseFloat(amount));
            }

            chart.update();

            form.reset();

            $.ajax({
                url: isIncome ? '/add_income' : '/add_expense',
                type: 'POST',
                data: { amount: amount, category: category, date: date },
                success: function (response) {
                    console.log(response.message);
                },
                error: function (xhr, status, error) {
                    alert('An error occurred while processing your request.');
                }
            });
        });
    }

    handleFormSubmit(incomeForm, incomePieChart, document.getElementById('income-tbody'), true);
    handleFormSubmit(expenseForm, expensePieChart, document.getElementById('expense-tbody'), false);
});
