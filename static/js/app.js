const watchlistForm = document.getElementById("watchlist-form");
const financeNoteForm = document.getElementById("finance-note-form");
const refreshAllButton = document.getElementById("refresh-all");

const watchlistTableBody = document.getElementById("watchlist-table-body");
const financeNotesTableBody = document.getElementById("finance-notes-table-body");

const watchlistMessage = document.getElementById("watchlist-message");
const financeNoteMessage = document.getElementById("finance-note-message");

function setMessage(element, text, type) {
    element.textContent = text;
    element.className = type ? `message ${type}` : "message";
}

function formatDate(value) {
    if (!value) {
        return "";
    }

    const date = new Date(value);
    if (Number.isNaN(date.getTime())) {
        return value;
    }

    return date.toLocaleString();
}

function displayValue(value) {
    return value || "";
}

function renderEmptyRow(tableBody, colspan, message) {
    tableBody.innerHTML = "";
    const row = document.createElement("tr");
    const cell = document.createElement("td");
    cell.colSpan = colspan;
    cell.className = "empty-cell";
    cell.textContent = message;
    row.appendChild(cell);
    tableBody.appendChild(row);
}

function appendCell(row, value) {
    const cell = document.createElement("td");
    cell.textContent = displayValue(value);
    row.appendChild(cell);
}

async function fetchJson(url, options) {
    const response = await fetch(url, options);

    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || `Request failed with status ${response.status}`);
    }

    return response.json();
}

async function loadWatchlist() {
    try {
        const items = await fetchJson("/watchlist/");
        watchlistTableBody.innerHTML = "";

        if (items.length === 0) {
            renderEmptyRow(watchlistTableBody, 5, "No watchlist items yet.");
            return;
        }

        items.forEach((item) => {
            const row = document.createElement("tr");
            appendCell(row, item.id);
            appendCell(row, item.ticker);
            appendCell(row, item.company_name);
            appendCell(row, item.notes);
            appendCell(row, formatDate(item.created_at));
            watchlistTableBody.appendChild(row);
        });
    } catch (error) {
        renderEmptyRow(watchlistTableBody, 5, "Could not load watchlist items.");
        console.error(error);
    }
}

async function loadFinanceNotes() {
    try {
        const notes = await fetchJson("/financenotes/");
        financeNotesTableBody.innerHTML = "";

        if (notes.length === 0) {
            renderEmptyRow(financeNotesTableBody, 5, "No finance notes yet.");
            return;
        }

        notes.forEach((note) => {
            const row = document.createElement("tr");
            appendCell(row, note.id);
            appendCell(row, note.ticker);
            appendCell(row, note.title);
            appendCell(row, note.content);
            appendCell(row, formatDate(note.created_at));
            financeNotesTableBody.appendChild(row);
        });
    } catch (error) {
        renderEmptyRow(financeNotesTableBody, 5, "Could not load finance notes.");
        console.error(error);
    }
}

async function createWatchlistItem(event) {
    event.preventDefault();
    setMessage(watchlistMessage, "Saving watchlist item...", "");

    const formData = new FormData(watchlistForm);
    const payload = {
        ticker: formData.get("ticker").trim().toUpperCase(),
        company_name: formData.get("company_name").trim() || null,
        notes: formData.get("notes").trim() || null,
    };

    try {
        await fetchJson("/watchlist/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        watchlistForm.reset();
        setMessage(watchlistMessage, "Watchlist item created.", "success");
        await loadWatchlist();
    } catch (error) {
        setMessage(watchlistMessage, "Could not create watchlist item.", "error");
        console.error(error);
    }
}

async function createFinanceNote(event) {
    event.preventDefault();
    setMessage(financeNoteMessage, "Saving finance note...", "");

    const formData = new FormData(financeNoteForm);
    const payload = {
        ticker: formData.get("ticker").trim().toUpperCase(),
        title: formData.get("title").trim(),
        content: formData.get("content").trim(),
    };

    try {
        await fetchJson("/financenotes/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        financeNoteForm.reset();
        setMessage(financeNoteMessage, "Finance note created.", "success");
        await loadFinanceNotes();
    } catch (error) {
        setMessage(financeNoteMessage, "Could not create finance note.", "error");
        console.error(error);
    }
}

watchlistForm.addEventListener("submit", createWatchlistItem);
financeNoteForm.addEventListener("submit", createFinanceNote);
refreshAllButton.addEventListener("click", () => {
    loadWatchlist();
    loadFinanceNotes();
});

loadWatchlist();
loadFinanceNotes();
