const cellRegistry = {}; // Maps cell name to its DOM element
const cellColorRegistry = {}; // Maps cell name to its current hex color string

const tablesContainer = document.getElementById('tables-container');

/**
 * Creates an HTML table from a 2D array of cell names and appends it to the container.
 * Supports rows with varying lengths.
 * @param {string} tableId - A unique ID for the table.
 * @param {string} title - The title to display above the table.
 * @param {string[][]} data - A 2D array. Each inner array is a row, containing cell name strings.
 * @param {string[]} [headers] - Optional array of header strings for the table.
 */
function createTable(tableId, title, data, headers) {
    if (!tablesContainer) {
        console.error("Tables container not found!");
        return;
    }

    const titleElement = document.createElement('h2');
    titleElement.className = 'table-title';
    titleElement.textContent = title;
    tablesContainer.appendChild(titleElement);

    const table = document.createElement('table');
    table.id = tableId;

    let numCols = 0; // Determine the number of columns for the table

    if (headers && headers.length > 0) {
        numCols = headers.length;
        const thead = table.createTHead();
        const headerRow = thead.insertRow();
        headers.forEach(headerText => {
            const th = document.createElement('th');
            th.textContent = headerText;
            headerRow.appendChild(th);
        });
    } else if (data && data.length > 0) {
        // If no headers, find the length of the longest row in data
        data.forEach(rowDataArray => {
            if (rowDataArray) { // Check if rowDataArray is defined
                numCols = Math.max(numCols, rowDataArray.length);
            }
        });
    }

    const tbody = table.createTBody();
    if (data && data.length > 0) { // Ensure data is not undefined or empty
        data.forEach(rowDataArray => {
            if (!rowDataArray) return; // Skip if a row itself is undefined/null

            const row = tbody.insertRow();
            for (let i = 0; i < numCols; i++) {
                const cell = row.insertCell();
                const cellName = rowDataArray[i]; // This will be undefined if the row is shorter than numCols

                if (cellName !== undefined && cellName !== null && typeof cellName === 'string' && cellName.trim() !== "") {
                    // If there's a cell name for this column in this row
                    cell.textContent = cellName;
                    cell.className = 'color-cell'; // Class for potential styling or selection
                    if (cellRegistry[cellName]) {
                        console.warn(`Duplicate cell name detected: "${cellName}". Operations may target the first registered instance.`);
                    }
                    cellRegistry[cellName] = cell;
                    cellColorRegistry[cellName] = null; // Initialize color
                } else {
                    // This cell is intentionally blank (row is shorter than numCols at this column index)
                    // You can leave it empty, or add a non-breaking space if you want to ensure it has dimensions
                    // cell.innerHTML = '&nbsp;';
                    // No need to add to cellRegistry or cellColorRegistry
                }
            }
        });
    }
    tablesContainer.appendChild(table);
}

/**
 * Finds and returns the DOM element for a given cell name.
 * @param {string} cellName - The unique name of the cell.
 * @returns {HTMLTableCellElement|null} The cell element or null if not found.
 */
function getCell(cellName) {
    const cell = cellRegistry[cellName];
    if (!cell) {
        console.error(`Cell with name "${cellName}" not found.`);
        return null;
    }
    return cell;
}

/**
 * Sets the background color of a cell and updates its text color for contrast.
 * @param {string} cellName - The name of the cell.
 * @param {string} hexColor - The hex color string (e.g., "#RRGGBB").
 */
function cellColor(cellName, hexColor) {
    const cell = getCell(cellName);
    if (cell && hexColor) {
        cell.style.backgroundColor = hexColor;
        cell.style.color = getContrastingTextColor(hexColor);
        cellColorRegistry[cellName] = hexColor.toLowerCase();
    } else if (cell && !hexColor) { // Reset color
        cell.style.backgroundColor = '';
        cell.style.color = '';
        cellColorRegistry[cellName] = null;
    }
}

/**
 * Retrieves the current hex color of a cell.
 * @param {string} cellName - The name of the cell.
 * @returns {string|null} The hex color string or null if not set.
 */
function getCellColor(cellName) {
    return cellColorRegistry[cellName] || null;
}

/**
 * Internal helper to get HSV color from a cell.
 * @param {string} cellName
 * @returns {object|null} HSV object {h, s, v} or null.
 */
function _getCellHsv(cellName) {
    const hex = getCellColor(cellName);
    if (!hex) {
        console.warn(`Color not set for cell "${cellName}" needed for analogy.`);
        return null;
    }
    const rgb = hexToRgb(hex);
    if (!rgb) return null;
    return rgbToHsv(rgb.r, rgb.g, rgb.b);
}

/**
 * Sets cell D's color so that A is to B as C is to D (in HSV space).
 * Colors for A, B, and C must be pre-defined using setCellColor.
 * @param {string} nameA
 * @param {string} nameB
 * @param {string} nameC
 * @param {string} nameD - The cell whose color will be set.
 */
function analogy4(nameA, nameB, nameC, nameD) {
    const hsvA = _getCellHsv(nameA);
    const hsvB = _getCellHsv(nameB);
    const hsvC = _getCellHsv(nameC);

    if (!hsvA || !hsvB || !hsvC) {
        console.error(`Cannot perform 4-element analogy for "${nameD}": Missing one or more source colors (A, B, or C).`);
        return;
    }

    // Calculate HSV shifts/deltas
    let deltaH = hsvB.h - hsvA.h;
    // Normalize hue delta to be in [-0.5, 0.5)
    if (deltaH > 0.5) deltaH -= 1.0;
    if (deltaH < -0.5) deltaH += 1.0;

    const deltaS = hsvB.s - hsvA.s;
    const deltaV = hsvB.v - hsvA.v;

    // Apply to hsvC
    let hD = (hsvC.h + deltaH + 1.0) % 1.0; // Ensure positive result before modulo
    let sD = Math.max(0, Math.min(1, hsvC.s + deltaS));
    let vD = Math.max(0, Math.min(1, hsvC.v + deltaV));

    const rgbD = hsvToRgb(hD, sD, vD);
    if (!rgbD) {
        console.error(`Failed to convert target HSV to RGB for "${nameD}".`);
        return;
    }
    const hexD = rgbToHex(rgbD.r, rgbD.g, rgbD.b);
    cellColor(nameD, hexD);
    console.log(`Set ${nameD} (${hexD}) based on: ${nameA}:${getCellColor(nameA)} -> ${nameB}:${getCellColor(nameB)} as ${nameC}:${getCellColor(nameC)} -> ${nameD}`);
}

/**
 * Sets cell C's color so that A is to B as B is to C (in HSV space).
 * This is a specific case of set4Analogy.
 * Colors for A and B must be pre-defined.
 * @param {string} nameA
 * @param {string} nameB
 * @param {string} nameC - The cell whose color will be set.
 */
function analogy3(nameA, nameB, nameC) {
    console.log(`Performing 3-element analogy for ${nameC}: ${nameA} is to ${nameB} as ${nameB} is to ${nameC}`);
    analogy4(nameA, nameB, nameB, nameC);
}

/**
 * Sets cell B's color to an interpolation between cell A and cell C in HSV space.
 * @param {string} nameA - Name of the first source cell.
 * @param {string} nameB - Name of the target cell to color.
 * @param {string} nameC - Name of the second source cell.
 * @param {number} t - Interpolation factor (0.0 for color A, 1.0 for color C).
 */
function interpolate(nameA, nameB, nameC, t) {
    const hsvA = _getCellHsv(nameA);
    const hsvC = _getCellHsv(nameC);

    if (!hsvA || !hsvC) {
        console.error(`Cannot interpolate for "${nameB}": Missing color for "${nameA}" or "${nameC}".`);
        return;
    }

    if (t < 0) t = 0;
    if (t > 1) t = 1;

    // Interpolate Hue (circular)
    let deltaH = hsvC.h - hsvA.h;
    if (deltaH > 0.5) {
        deltaH -= 1.0; // Go the shorter way around
    } else if (deltaH < -0.5) {
        deltaH += 1.0; // Go the shorter way around
    }
    const hB = (hsvA.h + deltaH * t + 1.0) % 1.0; // Ensure positive before modulo

    // Interpolate Saturation and Value (linear)
    const sB = hsvA.s + (hsvC.s - hsvA.s) * t;
    const vB = hsvA.v + (hsvC.v - hsvA.v) * t;

    // Clamp S and V
    const clampedSB = Math.max(0, Math.min(1, sB));
    const clampedVB = Math.max(0, Math.min(1, vB));

    const rgbB = hsvToRgb(hB, clampedSB, clampedVB);
    if (!rgbB) {
        console.error(`Failed to convert interpolated HSV to RGB for "${nameB}".`);
        return;
    }
    const hexB = rgbToHex(rgbB.r, rgbB.g, rgbB.b);
    cellColor(nameB, hexB);
    console.log(`Interpolated color for ${nameB} (${hexB}) from ${nameA} (${getCellColor(nameA)}) and ${nameC} (${getCellColor(nameC)}) at t=${t}`);
}


/**
 * Iterates through all 2x2 squares in a given table and attempts to complete
 * uncolored cells (that have text) by analogy if exactly three other cells in the square are colored.
 * @param {string} tableId - The ID of the table to process.
 */
function completeTable(tableId) {
    const table = document.getElementById(tableId);
    if (!table || !table.rows || table.rows.length < 2) {
        console.warn(`Table "${tableId}" not found or too small to complete.`);
        return;
    }

    const rowCount = table.rows.length;
    // Assuming all rows have the same number of cells due to createTable logic
    const colCount = table.rows[0].cells.length;

    if (colCount < 2) {
        console.warn(`Table "${tableId}" has too few columns to complete.`);
        return;
    }

    let completionsMade = 0;

    for (let r = 0; r <= rowCount - 1; r++) {
        for (let c = 0; c <= colCount - 1; c++) {
            for (let r2 = 0; r2 <= rowCount - 1; r2++) {
                for (let c2 = 0; c2 <= colCount - 1; c2++) {
                    if (r === r2 || c === c2) continue;
                    const cellsInSquare = [
                        [table.rows[r].cells[c], table.rows[r].cells[c2]],
                        [table.rows[r2].cells[c], table.rows[r2].cells[c2]]
                    ];

                    const cellData = cellsInSquare.flat().map(cellDOM => {
                        const name = cellDOM.textContent.trim();
                        return {
                            dom: cellDOM,
                            name: name,
                            color: name ? getCellColor(name) : null, // Only get color if there's a name
                            hasText: name !== ""
                        };
                    });

                    const uncoloredWithText = cellData.filter(cd => cd.hasText && !cd.color);
                    const coloredWithText = cellData.filter(cd => cd.hasText && cd.color);

                    if (coloredWithText.length === 3 && uncoloredWithText.length === 1) {
                        const targetCellData = uncoloredWithText[0];
                        const targetName = targetCellData.name;

                        // Identify cell positions for analogy (00, 01, 10, 11)
                        const c00 = cellData[0]; // Top-left of square
                        const c01 = cellData[1]; // Top-right
                        const c10 = cellData[2]; // Bottom-left
                        const c11 = cellData[3]; // Bottom-right

                        console.log(`Attempting to complete cell: "${targetName}" in table "${tableId}"`);

                        if (targetName === c11.name) { // Target is Bottom-Right (D)
                            // A:B :: C:D  => set4Analogy(A, B, C, D)
                            analogy4(c00.name, c01.name, c10.name, c11.name);
                        } else if (targetName === c10.name) { // Target is Bottom-Left (C)
                            // B:A :: D:C  => set4Analogy(B, A, D, C)
                            analogy4(c01.name, c00.name, c11.name, c10.name);
                        } else if (targetName === c01.name) { // Target is Top-Right (B)
                            // A:C :: D:B (using previous logic: C:D :: A:B) => set4Analogy(C,D,A,B)
                            // Let's verify: C(c10) is to D(c11) as A(c00) is to B(c01)
                            analogy4(c10.name, c11.name, c00.name, c01.name);
                        } else if (targetName === c00.name) { // Target is Top-Left (A)
                            // B:D :: C:A (using previous logic: D:C :: B:A) => set4Analogy(D,C,B,A)
                            // Let's verify: D(c11) is to C(c10) as B(c01) is to A(c00)
                            analogy4(c11.name, c10.name, c01.name, c00.name);
                        }
                        // Check if the color was actually set (it might not if source colors were missing for set4Analogy)
                        if (getCellColor(targetName)) {
                            completionsMade++;
                        }
                    }
                }
            }
        }
    }
    if (completionsMade > 0) {
        console.log(`${completionsMade} cell(s) completed in table "${tableId}". You might want to run completeTable again if completions enable further analogies.`);
    } else {
        console.log(`No cells could be automatically completed in table "${tableId}" in this pass.`);
    }
}