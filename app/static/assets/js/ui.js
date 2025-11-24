document.addEventListener('DOMContentLoaded', function(){
  const toggle = document.getElementById('sidebarToggle');
  const body = document.body;
  const backdrop = document.getElementById('sidebarBackdrop');

  // restore collapsed state
  try{
    const saved = localStorage.getItem('sipina:sidebarCollapsed');
    if(saved === 'true') body.classList.add('sidebar-collapsed');
  }catch(e){/* ignore */}

  function handleToggle(){
    if(window.innerWidth <= 576){
      // mobile: open/close overlay sidebar
      body.classList.toggle('sidebar-open');
    } else {
      // desktop/tablet: collapse/expand
      const collapsed = body.classList.toggle('sidebar-collapsed');
      try{ localStorage.setItem('sipina:sidebarCollapsed', collapsed ? 'true' : 'false'); }catch(e){}
    }
  }

  if(toggle){ toggle.addEventListener('click', handleToggle); }

  // backdrop click closes overlay
  if(backdrop){ backdrop.addEventListener('click', function(){ body.classList.remove('sidebar-open'); }); }

  // click outside to close overlay sidebar on mobile
  document.addEventListener('click', function(e){
    if(window.innerWidth <= 576 && body.classList.contains('sidebar-open')){
      const sidebar = document.querySelector('.sidebar');
      if(sidebar && !sidebar.contains(e.target) && toggle && !toggle.contains(e.target) && !backdrop.contains(e.target)){
        body.classList.remove('sidebar-open');
      }
    }
  });

  // handle resize: remove overlay if resized larger
  window.addEventListener('resize', function(){
    if(window.innerWidth > 576){ body.classList.remove('sidebar-open'); }
  });
});
