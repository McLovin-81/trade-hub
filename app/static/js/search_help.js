document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchInput");
    const suggestionsList = document.createElement("ul");
    suggestionsList.setAttribute("id", "suggestions");
    searchInput.parentNode.appendChild(suggestionsList);
    
    const searchForm = document.getElementById("searchForm");

   
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

                    // Send formular on click
                    suggestionItem.addEventListener("click", function () {
                        searchInput.value = symbol;
                        searchForm.submit();  
                    });
                    
                    suggestionsList.appendChild(suggestionItem);
                }
            });
        }
    });

    
    document.addEventListener("click", function (e) {
        if (!searchInput.contains(e.target)) {
            suggestionsList.innerHTML = "";  
        }
    });
});
