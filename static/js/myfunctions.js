document.addEventListener('DOMContentLoaded', function () {
  const toggleOpen = document.getElementById('toggleOpen');
  const toggleClose = document.getElementById('toggleClose');
  const hiddenMenu = document.getElementById('hiddenMenu');

  toggleOpen.addEventListener('click', function () {
    hiddenMenu.classList.toggle('hidden');
  });

  toggleClose.addEventListener('click', function () {
    hiddenMenu.classList.add('hidden');
  });
});
