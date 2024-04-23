
const columnsByTable = {
    purchase: ['sno' , 'reference_no', 'journal_date', 'purchase_date', 'expiry_date', 'purchaser_name', 'prefix', 'bond_no', 'denominations', 'branch_code', 'issue_teller'],
    redemption: ['sno' , 'encashment_date', 'party_name', 'account_no', 'prefix', 'bond_no', 'denominations', 'branch_code', 'pay_teller']
};


function updateColumns() {
    const tableSelect = document.getElementById('table');
    const columnSelect = document.getElementById('column');
    const selectedTable = tableSelect.value;

    columnSelect.innerHTML = '';

    columnsByTable[selectedTable].forEach(column => {
        const option = document.createElement('option');
        option.value = column;
        option.textContent = column;
        columnSelect.appendChild(option);
    });
}

updateColumns();



