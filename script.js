document.addEventListener("DOMContentLoaded", function () {
    const games = [
        { name: "Game 1", url: "games/game1.html" },
        { name: "Game 2", url: "games/game2.html" }
    ];

    const gameList = document.getElementById("gameList");
    const searchBar = document.getElementById("searchBar");

    function displayGames(filter = "") {
        gameList.innerHTML = "";
        games.filter(game => game.name.toLowerCase().includes(filter.toLowerCase()))
             .forEach(game => {
                let li = document.createElement("li");
                let a = document.createElement("a");
                a.href = game.url;
                a.textContent = game.name;
                li.appendChild(a);
                gameList.appendChild(li);
            });
    }

    searchBar.addEventListener("input", (e) => {
        displayGames(e.target.value);
    });

    displayGames();
});