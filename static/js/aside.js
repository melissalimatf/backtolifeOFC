// Seleciona os elementos do botão de abrir e fechar
const sidebarToggle = document.getElementById('sidebar-toggle');
const sidebarClose = document.getElementById('sidebar-close');
const sidebar = document.querySelector('.sidebar');

// Função para abrir a sidebar
sidebarToggle.addEventListener('click', () => {
    sidebar.classList.add('open');
});

// Função para fechar a sidebar
sidebarClose.addEventListener('click', () => {
    sidebar.classList.remove('open');
});
