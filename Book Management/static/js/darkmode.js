document.addEventListener("DOMContentLoaded", function () {
        const themeToggle = document.getElementById("toggle");
        const body = document.body;
        const buttons = document.querySelectorAll(".theme-button");

        function updateButtonTheme() {
            if (body.dataset.bsTheme === "dark") {
                buttons.forEach(btn => {
                    btn.classList.remove("btn-spiro-disco-ball");
                    btn.classList.add("btn-light");
                });
            } else {
                buttons.forEach(btn => {
                    btn.classList.remove("btn-light");
                    btn.classList.add("btn-spiro-disco-ball");
                })
                }
        }

        themeToggle.addEventListener("change", function () {
            body.dataset.bsTheme = this.checked ? "dark" : "light";
            localStorage.setItem("theme", this.checked ? "dark" : "light");
            updateButtonTheme();
        });

        // Load saved theme
        if (localStorage.getItem("theme") === "dark") {
            body.dataset.bsTheme = "dark";
            themeToggle.checked = true;
        }

        updateButtonTheme(); // Apply styles on page load
    });