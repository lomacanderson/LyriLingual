document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input');
    const resultsTableBody = document.getElementById('results-table').querySelector('tbody');
    let debounceTimeout;

    searchInput.addEventListener('input', () => {
        const query = searchInput.value.trim();
        clearTimeout(debounceTimeout);
        if (query.length > 0) {
            debounceTimeout = setTimeout(() => searchSongs(query), 500); // 500ms delay
        } else {
            resultsTableBody.innerHTML = ''; // Clear results if query is empty
        }
    });

    function searchSongs(query) {
        fetch(`/search?query=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => updateResults(data))
            .catch(error => console.error('Error:', error));
    }

    function updateResults(songs) {
        resultsTableBody.innerHTML = '';
        if (songs.length === 0) {
            resultsTableBody.innerHTML = '<tr><td colspan="4">No results found</td></tr>';
            return;
        }

        songs.forEach(song => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${song.title}</td>
                <td>${song.artist}</td>
                <td>${song.album}</td>
                <td><a href="/lyrics/${song.id}" class="action-button">View Lyrics</a></td>
            `;
            resultsTableBody.appendChild(row);
        });
    }
});
