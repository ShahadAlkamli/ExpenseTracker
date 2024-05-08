const balance = document.getElementById('balance');
const money_plus = document.getElementById('money-plus');
const money_minus = document.getElementById('money-minus');
const list = document.getElementById('list');
const form = document.getElementById('form');
const text = document.getElementById('text');
const amount = document.getElementById('amount');

let transactions = [];

// Add transaction
async function addTransaction(e) {
    e.preventDefault();
  
    console.log('Adding transaction...');
  
    if (text.value.trim() === '' || amount.value.trim() === '') {
      alert('Please add a text and amount');
      return;
    }
  
    const transaction = {
      text: text.value,
      amount: +amount.value
    };
  
    console.log('Transaction data:', transaction);
  
    try {
      const response = await fetch('/api/transactions/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(transaction)
      });
  
      console.log('Response:', response);
  
      const data = await response.json();
      console.log('New transaction:', data);
  
      transaction.id = data.id;
      transactions.push(transaction);
      addTransactionDOM(transaction);
      updateValues();
      text.value = '';
      amount.value = '';
    } catch (error) {
      console.error('Error adding transaction:', error);
    }
  }
  

// Add transactions to DOM list
function addTransactionDOM(transaction) {
  const sign = transaction.amount < 0 ? '-' : '+';

  const item = document.createElement('li');
  item.classList.add(transaction.amount < 0 ? 'minus' : 'plus');

  item.innerHTML = `
    ${transaction.text} <span>${sign}${Math.abs(transaction.amount)}</span> <button class="delete-btn" onclick="removeTransaction(${transaction.id})">x</button>
  `;

  list.appendChild(item);
}

// Update the balance, income and expense
function updateValues() {
  const amounts = transactions.map(transaction => transaction.amount);

  const total = amounts.reduce((acc, item) => (acc += item), 0).toFixed(2);
  const income = amounts.filter(item => item > 0).reduce((acc, item) => (acc += item), 0).toFixed(2);
  const expense = (amounts.filter(item => item < 0).reduce((acc, item) => (acc += item), 0) * -1).toFixed(2);

  balance.innerText = `$${total}`;
  money_plus.innerText = `$${income}`;
  money_minus.innerText = `$${expense}`;
}

async function removeTransaction(id) {
    try {
        await fetch(`/api/transactions/${id}/`, {
            method: 'DELETE'
        });

        // Remove the transaction from the transactions array
        transactions = transactions.filter(transaction => transaction.id !== id);

        // Update the DOM to remove the transaction
        list.innerHTML = ''; // Clear the list
        transactions.forEach(addTransactionDOM); // Re-render the list without the deleted transaction

        // Update the balance, income, and expense
        updateValues();
    } catch (error) {
        console.error('Error deleting transaction:', error);
    }
}



  

// Init app
async function init() {
  try {
    const response = await fetch('/api/transactions/');
    transactions = await response.json();
    list.innerHTML = '';
    transactions.forEach(addTransactionDOM);
    updateValues();
  } catch (error) {
    console.error('Error initializing app:', error);
  }
}

init();

form.addEventListener('submit', addTransaction);
