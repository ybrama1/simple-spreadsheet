/**
 * Simple Spreadsheet - Main JavaScript Controller
 * Handles UI interactions and communication with the Python backend API
 */

// ===== GLOBAL VARIABLES =====
let currentRows = 4; // Current number of rows in the spreadsheet
let currentCols = 4; // Current number of columns in the spreadsheet

// ===== INITIALIZATION =====
/**
 * Initialize the spreadsheet when the page loads
 */
document.addEventListener('DOMContentLoaded', function() {
    createSpreadsheet();
});

// ===== SPREADSHEET CREATION =====
/**
 * Creates a new spreadsheet with the specified dimensions
 * Validates input and creates both input and result tables
 */
function createSpreadsheet() {
    // Get dimension values from input fields
    const rows = parseInt(document.getElementById('rows').value);
    const cols = parseInt(document.getElementById('cols').value);
    
    // Validate dimensions
    if (rows < 1 || cols < 1 || rows > 10 || cols > 10) {
        showMessage('Please enter valid dimensions (1-10)', 'error');
        return;
    }

    // Update global variables
    currentRows = rows;
    currentCols = cols;

    // Create both input and result tables
    createTable('inputSpreadsheet', rows, cols, true);  // Editable table
    createTable('resultSpreadsheet', rows, cols, false); // Read-only table
}

/**
 * Creates a single table (either input or result)
 * @param {string} containerId - ID of the container element
 * @param {number} rows - Number of rows to create
 * @param {number} cols - Number of columns to create
 * @param {boolean} editable - Whether cells should be editable
 */
function createTable(containerId, rows, cols, editable) {
    const container = document.getElementById(containerId);
    const table = document.createElement('table');
    
    // Create header row with column letters (A, B, C, ...)
    const headerRow = document.createElement('tr');
    headerRow.appendChild(document.createElement('th')); // Empty corner cell
    
    for (let j = 0; j < cols; j++) {
        const th = document.createElement('th');
        th.textContent = String.fromCharCode(65 + j); // Convert 0->A, 1->B, etc.
        headerRow.appendChild(th);
    }
    table.appendChild(headerRow);

    // Create data rows
    for (let i = 0; i < rows; i++) {
        const row = document.createElement('tr');
        
        // Create row header with row number
        const rowHeader = document.createElement('td');
        rowHeader.className = 'row-header';
        rowHeader.textContent = i + 1; // 1-based row numbering
        row.appendChild(rowHeader);
        
        // Create data cells
        for (let j = 0; j < cols; j++) {
            const cell = document.createElement('td');
            
            if (editable) {
                // Create input field for editable cells
                const input = document.createElement('input');
                input.type = 'text';
                input.id = `cell-${i}-${j}`; // Unique ID for each cell
                cell.appendChild(input);
            } else {
                // Create read-only result cell
                cell.className = 'result-cell';
                cell.id = `result-${i}-${j}`; // Unique ID for each result cell
            }
            
            row.appendChild(cell);
        }
        table.appendChild(row);
    }
    
    // Replace container content with new table
    container.innerHTML = '';
    container.appendChild(table);
}

// ===== DATA MANAGEMENT =====
/**
 * Extracts data from all input cells into a 2D array
 * @returns {Array<Array<string>>} Matrix of cell values
 */
function getSpreadsheetData() {
    const data = [];
    for (let i = 0; i < currentRows; i++) {
        const row = [];
        for (let j = 0; j < currentCols; j++) {
            const input = document.getElementById(`cell-${i}-${j}`);
            row.push(input ? input.value : ''); // Use empty string if input not found
        }
        data.push(row);
    }
    return data;
}

/**
 * Displays evaluation results in the result table
 * @param {Array<Array<number>>} results - Matrix of evaluated values
 */
function displayResults(results) {
    for (let i = 0; i < currentRows; i++) {
        for (let j = 0; j < currentCols; j++) {
            const cell = document.getElementById(`result-${i}-${j}`);
            if (cell && results[i] && results[i][j] !== undefined) {
                cell.textContent = results[i][j];
            }
        }
    }
}

// ===== API COMMUNICATION =====
/**
 * Sends spreadsheet data to Python backend for evaluation
 * Handles API communication and result display
 */
async function evaluateSpreadsheet() {
    try {
        // Get current spreadsheet data
        const matrix = getSpreadsheetData();
        
        // Send POST request to evaluation API
        const response = await fetch('/api/evaluate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ matrix: matrix })
        });

        // Parse response
        const data = await response.json();

        if (data.success) {
            // Display results and success message
            displayResults(data.result);
            showMessage('✅ Spreadsheet evaluated successfully!', 'success');
        } else {
            // Display error message from API
            showMessage('❌ Error: ' + data.error, 'error');
        }
    } catch (error) {
        // Handle network or parsing errors
        showMessage('❌ Network error: ' + error.message, 'error');
    }
}

// ===== EXAMPLE DATA =====
/**
 * Loads a predefined example into the spreadsheet
 * Useful for demonstrating functionality
 */
function loadExample() {
    // Clear existing data first
    clearSpreadsheet();
    
    // Set dimensions to match example
    document.getElementById('rows').value = 3;
    document.getElementById('cols').value = 2;
    createSpreadsheet();
    
    // Define example data showing various formula types
    const exampleData = [
        ['=B2+5', '=A1-3.5'],  // Formula with addition and subtraction
        ['=A1', '42'],         // Cell reference and number
        ['3.14', '=B2']       // Number and cell reference
    ];

    // Load example data into input fields
    for (let i = 0; i < exampleData.length; i++) {
        for (let j = 0; j < exampleData[i].length; j++) {
            const input = document.getElementById(`cell-${i}-${j}`);
            if (input) {
                input.value = exampleData[i][j];
            }
        }
    }
    
    showMessage('📝 Example loaded! Click "Evaluate" to see the results.', 'success');
}

// ===== UTILITY FUNCTIONS =====
/**
 * Clears all data from both input and result tables
 */
function clearSpreadsheet() {
    for (let i = 0; i < currentRows; i++) {
        for (let j = 0; j < currentCols; j++) {
            // Clear input field
            const input = document.getElementById(`cell-${i}-${j}`);
            if (input) input.value = '';
            
            // Clear result cell
            const result = document.getElementById(`result-${i}-${j}`);
            if (result) result.textContent = '';
        }
    }
    showMessage('🗑️ Spreadsheet cleared', 'success');
}

/**
 * Displays a temporary message to the user
 * @param {string} message - Message text to display
 * @param {string} type - Message type ('success' or 'error')
 */
function showMessage(message, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.innerHTML = `<div class="${type}">${message}</div>`;
    
    // Auto-hide message after 3 seconds
    setTimeout(() => {
        messageDiv.innerHTML = '';
    }, 3000);
}

// ===== KEYBOARD SHORTCUTS =====
/**
 * Handle keyboard shortcuts for improved user experience
 */
document.addEventListener('keydown', function(e) {
    // Ctrl+Enter: Evaluate spreadsheet
    if (e.ctrlKey && e.key === 'Enter') {
        e.preventDefault(); // Prevent default browser behavior
        evaluateSpreadsheet();
    }
});
