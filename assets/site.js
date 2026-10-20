(function(){
  var root=document.querySelector('script[src$="site.js"]').getAttribute('src').replace('assets/site.js','');
  fetch(root+'stats.json',{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).then(function(d){
    if(!d) return;
    document.querySelectorAll('[data-stat]').forEach(function(el){var k=el.dataset.stat;if(d[k]!=null)el.textContent=d[k]});
    if(d.papers) document.querySelectorAll('[data-pub]').forEach(function(el){var n=d.papers[el.dataset.pub];if(n==null)return;el.innerHTML=(n>0?n:'–')+'<small>'+(n>0?'cited':'new')+'</small>'});
  }).catch(function(){});
  var b=document.getElementById('copyEmail');
  if(b) b.addEventListener('click',function(){
    var t=document.getElementById('email').textContent;
    function sel(){var r=document.createRange();r.selectNodeContents(document.getElementById('email'));var s=getSelection();s.removeAllRanges();s.addRange(r);b.textContent='Selected'}
    try{navigator.clipboard.writeText(t).then(function(){b.textContent='Copied';setTimeout(function(){b.textContent='Copy'},1600)},sel)}catch(e){sel()}
  });
  var last=null;
  function close(){var l=document.querySelector('.lb');if(l){l.remove();document.body.style.overflow='';if(last)last.focus()}}
  function open(img){
    last=img;var fc=img.closest('figure')&&img.closest('figure').querySelector('figcaption');
    var l=document.createElement('div');l.className='lb';l.setAttribute('role','dialog');l.setAttribute('aria-modal','true');l.setAttribute('aria-label','Enlarged photo');
    var c=document.createElement('button');c.type='button';c.textContent='Close';c.onclick=close;
    var big=document.createElement('img');big.src=img.currentSrc||img.src;big.alt=img.alt;
    var p=document.createElement('p');p.textContent=fc?fc.textContent:img.alt;
    l.append(c,big,p);l.addEventListener('click',function(e){if(e.target===l||e.target===big)close()});
    document.body.appendChild(l);document.body.style.overflow='hidden';c.focus();
  }
  document.querySelectorAll('.project figure img, .portrait img').forEach(function(img){
    img.classList.add('zoomable');img.tabIndex=0;img.setAttribute('role','button');
    img.addEventListener('click',function(){open(img)});
    img.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();open(img)}});
  });
  document.addEventListener('keydown',function(e){if(e.key==='Escape')close()});
})();
