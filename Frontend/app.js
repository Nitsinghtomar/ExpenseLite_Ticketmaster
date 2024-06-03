document.getElementById('expense-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const expense = {
        date: document.getElementById('date').value,
        amount: document.getElementById('amount').value,
        category: document.getElementById('category').value,
        recipient: document.getElementById('recipient').value,
    };

    let expenses = JSON.parse(localStorage.getItem('expenses')) || [];
    expenses.push(expense);
    localStorage.setItem('expenses', JSON.stringify(expenses));

    displayExpenses();
    renderChart(); // Update the chart after adding an expense
    
    // Clear the form inputs directly
    document.getElementById('date').value = '';
    document.getElementById('amount').value = '';
    document.getElementById('category').value = '';
    document.getElementById('recipient').value = '';
});

document.getElementById('clear-all').addEventListener('click', function() {
    localStorage.removeItem('expenses');
    displayExpenses();
    renderChart(); // Update the chart after clearing all expenses
});

function displayExpenses() {
    const filterDate = document.getElementById('filter-date').value;
    const filterCategory = document.getElementById('filter-category').value;

    const expenses = JSON.parse(localStorage.getItem('expenses')) || [];
    const filteredExpenses = expenses.filter(expense => {
        return (!filterDate || expense.date === filterDate) &&
               (!filterCategory || expense.category === filterCategory);
    });

    const expenseTableBody = document.getElementById('expense-table-body');
    expenseTableBody.innerHTML = '';

    filteredExpenses.forEach((expense, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap">${expense.date}</td>
            <td class="px-6 py-4 whitespace-nowrap">${expense.amount}</td>
            <td class="px-6 py-4 whitespace-nowrap">${expense.category}</td>
            <td class="px-6 py-4 whitespace-nowrap">${expense.recipient}</td>
            <td class="px-6 py-4 whitespace-nowrap">
                <button class="delete-expense px-2 py-1 bg-red-500 text-white rounded-md" data-index="${index}">Delete</button>
            </td>
        `;
        expenseTableBody.appendChild(row);
    });

    updateCategoryFilterOptions();
    addDeleteEventListeners();
}

function addDeleteEventListeners() {
    const deleteButtons = document.querySelectorAll('.delete-expense');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const index = this.getAttribute('data-index');
            let expenses = JSON.parse(localStorage.getItem('expenses')) || [];
            expenses.splice(index, 1);
            localStorage.setItem('expenses', JSON.stringify(expenses));
            displayExpenses();
            renderChart(); // Update the chart after deleting an expense
        });
    });
}

function updateCategoryFilterOptions() {
    const expenses = JSON.parse(localStorage.getItem('expenses')) || [];
    const categories = [...new Set(expenses.map(expense => expense.category))];
    
    const filterCategory = document.getElementById('filter-category');
    filterCategory.innerHTML = '<option value="">All Categories</option>';

    categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category;
        option.textContent = category;
        filterCategory.appendChild(option);
    });
}

window.expenseChart=new Chart(document.getElementById("expenseChart"),{type:"bar",data:{labels:[],datasets:[{label:"Expenses by Category",data:[],backgroundColor:"rgba(75, 192, 192, 0.2)",borderColor:"rgba(75, 192, 192, 1)",borderWidth:1}]},options:{plugins:{legend:{display:!1}}}});function renderChart(){const expenses=JSON.parse(localStorage.getItem("expenses"))||[];const categories=[...new Set(expenses.map(expense=>expense.category))];const data=categories.map(category=>expenses.filter(expense=>expense.category===category).reduce((total,expense)=>total+parseFloat(expense.amount),0));const ctx=document.getElementById("expenseChart").getContext("2d");null==window.expenseChart?window.expenseChart=new Chart(ctx,{type:"bar",data:{labels:categories,datasets:[{label:"Expenses by Category",data:data,backgroundColor:"rgba(75, 192, 192, 0.2)",borderColor:"rgba(75, 192, 192, 1)",borderWidth:1}]},options:{plugins:{legend:{display:!1}}}}):(window.expenseChart.data.labels=categories,window.expenseChart.data.datasets[0].data=data,window.expenseChart.update())}window.onload=function(){displayExpenses(),renderChart(),updateCategoryFilterOptions()};
function renderChart() {
    const expenses = JSON.parse(localStorage.getItem('expenses')) || [];
    const categories = [...new Set(expenses.map(expense => expense.category))];
    const data = categories.map(category => {
        return expenses.filter(expense => expense.category === category)
                       .reduce((total, expense) => total + parseFloat(expense.amount), 0);
    });

    const ctx = document.getElementById('expenseChart').getContext('2d');

    // If there's an existing chart, update its data
    if (window.expenseChart) {
        window.expenseChart.data.labels = categories;
        window.expenseChart.data.datasets[0].data = data;
        window.expenseChart.update();
    } else {
        // If there's no existing chart, create a new chart
        window.expenseChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: categories,
                datasets: [{
                    label: 'Expenses by Category',
                    data: data,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                plugins: {
                    legend: {
                        display: false // Hide the legend
                    }
                }
            }
        });
    }
}

window.onload = function() {
    displayExpenses();
    renderChart();
    updateCategoryFilterOptions();
};
