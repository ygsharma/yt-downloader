// Wait for the entire page to load
document.addEventListener('DOMContentLoaded', function () {
    // Function to update dropdown button text
    function updateDropdownButtonText(dropdownItem) {
        var text = dropdownItem.textContent;
        var dropdownButton = dropdownItem.closest('.dropdown').querySelector('.dropdown-toggle');
        dropdownButton.textContent = text;
    }

    // Select all dropdown items
    var dropdownItems = document.querySelectorAll('.dropdown-menu .dropdown-item');

    // Add click event to each dropdown item
    dropdownItems.forEach(function(item) {
        item.addEventListener('click', function() {
            updateDropdownButtonText(this);
        });
    });
});

