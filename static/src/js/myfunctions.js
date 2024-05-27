var toggleOpen = document.getElementById('toggleOpen');
var toggleClose = document.getElementById('toggleClose');
var collapseMenu = document.getElementById('collapseMenu');

// Function to close the menu
function closeMenu() {
  collapseMenu.style.display = 'none';
}

function handleClick(event) {
  // Check if clicked element is the toggle buttons
  if (event.target === toggleOpen || event.target === toggleClose) {
    // Toggle menu visibility based on current state
    collapseMenu.style.display = collapseMenu.style.display === 'block' ? 'none' : 'block';
  } else {
    // Clicked outside the menu, close it
    closeMenu();
  }
}

// Add event listener to document (or body) for outside clicks
document.addEventListener('click', handleClick);

// Event listeners for toggle buttons remain the same
toggleOpen.addEventListener('click', handleClick);
toggleClose.addEventListener('click', handleClick);
