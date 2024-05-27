<script></script>
var toggleOpen = document.getElementById('toggleOpen');
var collapseMenu = document.getElementById('collapseMenu');
var hiddenMenu = document.getElementById('hiddenMenu');

function handleClick() {
  collapseMenu.style.display = collapseMenu.style.display === 'block' ? 'none' : 'block';
}

toggleOpen.addEventListener('click', handleClick);

// Add event listener for closing on outside click
document.addEventListener('click', function(event) {
  const clickedElement = event.target;
  // Check if clicked outside the menu and menu is open
  if (collapseMenu.style.display === 'block' && 
      !clickedElement.classList.contains('flex') && // Check for menu container class
      !clickedElement.classList.contains('items-center') && // Additional classes if needed
      !clickedElement.classList.contains('ml-auto') &&
      !clickedElement.closest('.flex.items-center.ml-auto')) { // Check for ancestor with class
    collapseMenu.style.display = 'none';
  }
});
