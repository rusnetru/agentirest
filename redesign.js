function getCategoryBadge(s){if(s.is_mcp)return{label:"MCP",cls:"cat-mcp"};var c=(s.category||"").toLowerCase();if(c.indexOf("security")>=0)return{label:"Безопасность",cls:"cat-security"};if(c.indexOf("browser")>=0)return{label:"Браузеры",cls:"cat-browser"};if(c.indexOf("discovery")>=0)return{label:"Каталоги",cls:"cat-discovery"};if(c.indexOf("devtool")>=0||c.indexOf("standards")>=0)return{label:"Инструменты",cls:"cat-devtools"};return{label:"SKILL.md",cls:"cat-skill"}}

function renderTrending(){var t=allSkills.filter(function(s){return s.is_new}).slice(0,5);if(t.length<3)t=allSkills.slice(0,5);if(!t.length)return;var el=document.getElementById("trending-grid");el.innerHTML=t.map(function(s,i){var b=getCategoryBadge(s);var ih="";if(s.install){ih='<div class="skill-install"><button class="install-toggle" onclick="toggleInstall(\'t'+i+'\')">⚡ Установить</button><div class="install-code" id="install-t'+i+'">'+s.install+'</div></div>'}return'<div class="skill-item"><div class="skill-name">'+(s.url?'<a href="'+s.url+'" target="_blank">'+s.name+'</a>':s.name)+'</div><div class="skill-meta">'+s.source+' &middot; '+s.category+'</div><div class="skill-desc">'+s.desc+'</div><div class="skill-tags"><span class="cat-badge '+b.cls+'">'+b.label+'</span>'+(s.secure?'<span class="tag tag-secure">Проверен</span>':'')+'<span class="tag tag-new">Новое</span></div>'+ih+'</div>'}).join("");document.getElementById("trending-section").style.display=""}

function setCategoryTab(btn,cat){var w=btn.classList.contains("active");document.querySelectorAll(".cat-tab").forEach(function(b){b.classList.remove("active")});if(w){document.getElementById("filter-category").value=""}else{btn.classList.add("active");document.getElementById("filter-category").value=cat}filterSkills()}

document.addEventListener('DOMContentLoaded', function(){
  var dc = document.getElementById('digest-content');
  if(dc) dc.classList.add('skills-grid');
});
