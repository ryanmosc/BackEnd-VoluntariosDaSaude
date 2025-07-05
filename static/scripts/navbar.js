document.addEventListener('DOMContentLoaded', () => {
  const navItems = document.querySelectorAll('#nav_list .nav-item a');


  const routeMap = {
    '/': 'index.html',
    '/sobre_nos': 'sobreNos.html',
    '/transparencia': 'transparencia.html',
    '/fale_conosco': 'fale_conosco.html',
    '/seja_voluntario': 'seja_voluntario.html',
    '/doacao': 'doacao.html'
  };


  document.querySelectorAll('#nav_list .nav-item').forEach(item => {
    item.classList.remove('active');
  });


  let currentPath = window.location.pathname;
  if (currentPath === '' || currentPath === '/') {
    currentPath = '/';
  }

 
  const currentPage = routeMap[currentPath] || currentPath.split('/').pop();

 
  navItems.forEach(link => {
    const href = link.getAttribute('href');


    if (href.startsWith('#')) return;


    if (href === currentPage || href === currentPath || routeMap[href] === currentPage) {
      link.parentElement.classList.add('active');
    }
  });
});