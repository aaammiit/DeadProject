function withAllRowsVisible(callback) {
    const tableBody = document.getElementById('table-body');
    const hiddenRows = [];

    // Unhide all rows temporarily
    tableBody.querySelectorAll('tr').forEach(row => {
        if (row.style.display === 'none') {
            hiddenRows.push(row);
            row.style.display = 'table-row';
        }
    });

    // Run the export
    callback();

    // Re-hide rows after export
    hiddenRows.forEach(row => row.style.display = 'none');
}

// Excel Export
document.getElementById('exportExcel').addEventListener('click', function () {
    withAllRowsVisible(() => {
        const table = document.querySelector('table');
        const wb = XLSX.utils.table_to_book(table, { sheet: "Krima Sheet" });
        XLSX.writeFile(wb, 'KrimaData.xlsx');
    });
});

// PDF Export
document.getElementById('exportPDF').addEventListener('click', function () {
    withAllRowsVisible(() => {
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF({ orientation: "landscape" });

        doc.autoTable({
            html: 'table',
            styles: { fontSize: 7 },
            headStyles: { fillColor: [6, 37, 53] },
            margin: { top: 10 }
        });

        doc.save('KrimaData.pdf');
    });
});