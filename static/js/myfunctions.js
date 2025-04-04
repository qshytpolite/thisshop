// Mobile menu toggle
document.getElementById('mobile-menu-btn').addEventListener('click', () => {
  const menu = document.getElementById('mobile-menu');
  menu.classList.toggle('hidden');
});

// Mobile search toggle
document.getElementById('mobile-search-btn').addEventListener('click', () => {
  const search = document.getElementById('mobile-search');
  search.classList.toggle('hidden');
});

// Close menus when clicking outside
document.addEventListener('click', (e) => {
  if(!e.target.closest('#mobile-menu') && !e.target.closest('#mobile-menu-btn')) {
      document.getElementById('mobile-menu').classList.add('hidden');
  }
  if(!e.target.closest('#mobile-search') && !e.target.closest('#mobile-search-btn')) {
      document.getElementById('mobile-search').classList.add('hidden');
  }
});