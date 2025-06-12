document.addEventListener('DOMContentLoaded', () => {
    const accountIcon = document.querySelector('.js-show-modal-account');
    const dropdownMenu = document.querySelector('.dropdown-menu-user');
  
    accountIcon.addEventListener('click', (event) => {
      // Prevent toggling if a link is clicked
      if (event.target.tagName !== 'A') {
        dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
        event.preventDefault();
      }
    });
  
    // Close dropdown when clicking outside
    document.addEventListener('click', (event) => {
      if (!accountIcon.contains(event.target)) {
        dropdownMenu.style.display = 'none';
      }
    });
  });
  
  