async function submitQuery() {
    const queryInput = document.getElementById('queryInput');
    const resultsContainer = document.getElementById('results');
    const query = queryInput.value.trim();

    if (!query) {
        alert('Please enter a query');
        return;
    }

    try {
        // Show loading state
        resultsContainer.innerHTML = '<p>Processing your query...</p>';
        resultsContainer.classList.add('active');

        const response = await fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to process query');
        }

        // Display results
        displayResults(data);
    } catch (error) {
        resultsContainer.innerHTML = `
            <div class="error">
                <p>Error: ${error.message}</p>
            </div>
        `;
    }
}

function displayResults(data) {
    const resultsContainer = document.getElementById('results');
    
    if (!data || !data.results || data.results.length === 0) {
        resultsContainer.innerHTML = '<p>No results found</p>';
        return;
    }

    let tableHTML = '<table class="results-table"><thead><tr>';
    
    // Create table headers from the first result's keys
    const headers = Object.keys(data.results[0]);
    headers.forEach(header => {
        tableHTML += `<th>${formatHeader(header)}</th>`;
    });
    tableHTML += '</tr></thead><tbody>';

    // Add table rows
    data.results.forEach(row => {
        tableHTML += '<tr>';
        headers.forEach(header => {
            tableHTML += `<td>${row[header]}</td>`;
        });
        tableHTML += '</tr>';
    });

    tableHTML += '</tbody></table>';

    // Add SQL query for reference
    const sqlQueryHTML = data.sql_query ? 
        `<div class="sql-query">
            <p>Generated SQL Query:</p>
            <pre>${data.sql_query}</pre>
        </div>` : '';

    resultsContainer.innerHTML = sqlQueryHTML + tableHTML;
}

function formatHeader(header) {
    // Convert snake_case to Title Case
    return header
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

// Add event listener for Enter key
document.getElementById('queryInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        submitQuery();
    }
});

// Add these styles dynamically
const style = document.createElement('style');
style.textContent = `
    .results-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }

    .results-table th,
    .results-table td {
        padding: 12px;
        text-align: left;
        border: 1px solid #dfe1e5;
    }

    .results-table th {
        background-color: #f8f9fa;
        color: #1a73e8;
        font-weight: bold;
    }

    .results-table tr:nth-child(even) {
        background-color: #f8f9fa;
    }

    .sql-query {
        margin: 20px 0;
        padding: 15px;
        background-color: #f8f9fa;
        border-radius: 4px;
    }

    .sql-query pre {
        background-color: #fff;
        padding: 10px;
        border-radius: 4px;
        overflow-x: auto;
    }

    .error {
        color: #d93025;
        padding: 10px;
        border-radius: 4px;
        background-color: #fce8e6;
    }
`;
document.head.appendChild(style);
