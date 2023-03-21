document.addEventListener("DOMContentLoaded", function() {
    const toggleSwitch = document.getElementById("toggleSwitch");
    toggleSwitch.addEventListener("change", toggleDarkMode);

    function toggleDarkMode() {
        if (toggleSwitch.checked) {
            document.body.classList.add("dark-mode");
        } else {
            document.body.classList.remove("dark-mode");
        }
    }
});
