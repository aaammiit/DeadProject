document.getElementById('toggle-view-btn').addEventListener('change', function () {
    var tableView = document.getElementById('table-view');
    var exportView = document.getElementById('export-view');
    var cardView = document.getElementById('card-view');
    var label = document.getElementById('toggle-label');

    if (this.checked) {
        cardView.style.display = 'none';
        tableView.style.display = 'block';
        exportView.style.display = 'block';
        label.style.display ='none'; // Hide text in Table View
    } else {
        cardView.style.display = 'block';
        tableView.style.display = 'none';
        exportView.style.display = 'none';
        label.style.display ='none';// Show text only in Card View
    }
});

// Pagination
let currentPage = 1;
const rowsPerPage = 10;
const tableRows = document.querySelectorAll(".table-row");
const totalPages = Math.ceil(tableRows.length / rowsPerPage);

function showPage(page) {
    let start = (page - 1) * rowsPerPage;
    let end = start + rowsPerPage;

    tableRows.forEach((row, index) => {
        row.style.display = (index >= start && index < end) ? "table-row" : "none";
    });

    document.getElementById("page-info").innerText = `Page ${page}`;
    document.getElementById("prev-page").disabled = (page === 1);
    document.getElementById("next-page").disabled = (page === totalPages);
}

document.getElementById("prev-page").addEventListener("click", function () {
    if (currentPage > 1) {
        currentPage--;
        showPage(currentPage);
    }
});

document.getElementById("next-page").addEventListener("click", function () {
    if (currentPage < totalPages) {
        currentPage++;
        showPage(currentPage);
    }
});

// Initialize table pagination
showPage(1);
