document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchInput");
    const suggestionsList = document.createElement("ul");
    searchInput.parentNode.appendChild(suggestionsList);

    // Das Dictionary, das in der main.html als JSON eingebettet wird
    const daxAktien = JSON.parse(document.getElementById("daxAktienData").textContent);

    searchInput.addEventListener("input", function () {
        const query = searchInput.value.toLowerCase();
        suggestionsList.innerHTML = "";

        if (query.length > 0) {
            Object.keys(daxAktien).forEach(function (name) {
                const symbol = daxAktien[name];
                if (name.toLowerCase().includes(query) || symbol.toLowerCase().includes(query)) {
                    const suggestionItem = document.createElement("li");
                    suggestionItem.textContent = `${name} (${symbol})`;
                    suggestionItem.addEventListener("click", function () {
                        searchInput.value = symbol;
                        suggestionsList.innerHTML = "";  // Vorschläge leeren
                    });
                    suggestionsList.appendChild(suggestionItem);
                }
            });
        }
    });
});