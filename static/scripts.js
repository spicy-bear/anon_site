document.addEventListener("DOMContentLoaded", function () {
    const darkModeToggle = document.getElementById("dark-mode-toggle");

    // Check the stored dark mode state on page load
    if (localStorage.getItem("darkMode") === "enabled") {
        document.documentElement.classList.add("dark-mode");
    }

    darkModeToggle.addEventListener("click", function () {
        document.documentElement.classList.toggle("dark-mode");

        // Save the dark mode state to localStorage
        if (document.documentElement.classList.contains("dark-mode")) {
            localStorage.setItem("darkMode", "enabled");
        } else {
            localStorage.removeItem("darkMode");
        }
    });

    document.getElementById("url_form").addEventListener("submit", function (event) {
        event.preventDefault();
        const urlInput = document.getElementById("url_input");
        if (!urlInput.value.trim()) {
            alert("Please enter a URL");
        } else {
            event.target.submit();
        }
    });

    document.getElementById('change-theme-btn').addEventListener('click', function () {
        let darkThemeEnabled = document.body.classList.toggle('dark-theme');
        localStorage.setItem('dark-theme-enabled', darkThemeEnabled);
    });

    if (JSON.parse(localStorage.getItem('dark-theme-enabled'))) {
        document.body.classList.add('dark-theme');
    }
});
