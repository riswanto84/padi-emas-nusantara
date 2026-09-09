(function(){
const shell=document.querySelector('.app-shell'),toggle=document.querySelector('[data-sidebar-toggle]'),backdrop=document.querySelector('[data-sidebar-backdrop]');
if(!shell||!toggle)return;const key='padi-emas-sidebar-collapsed';const isMobile=()=>window.matchMedia('(max-width:760px)').matches;
function sync(){if(isMobile()){shell.classList.remove('sidebar-collapsed');return} if(localStorage.getItem(key)==='1')shell.classList.add('sidebar-collapsed');else shell.classList.remove('sidebar-collapsed')}
toggle.addEventListener('click',()=>{if(isMobile())shell.classList.toggle('sidebar-open');else{shell.classList.toggle('sidebar-collapsed');localStorage.setItem(key,shell.classList.contains('sidebar-collapsed')?'1':'0')}});
backdrop?.addEventListener('click',()=>shell.classList.remove('sidebar-open'));
document.querySelectorAll('.sidebar .nav-item').forEach(a=>a.addEventListener('click',()=>{if(isMobile())shell.classList.remove('sidebar-open')}));
window.addEventListener('resize',sync);sync();
})();

(function(){
  const card=document.querySelector('[data-weather-card]');
  const list=document.querySelector('[data-forecast-list]');
  if(!card || !list) return;
  const api='/api/cuaca/';
  const iconMap={0:'☀️',1:'🌤️',2:'⛅',3:'☁️',45:'🌫️',48:'🌫️',51:'🌦️',53:'🌦️',55:'🌧️',56:'🌧️',57:'🌧️',61:'🌦️',63:'🌧️',65:'🌧️',66:'🌧️',67:'🌧️',71:'🌨️',73:'🌨️',75:'❄️',77:'🌨️',80:'🌦️',81:'🌧️',82:'⛈️',85:'🌨️',86:'🌨️',95:'⛈️',96:'⛈️',99:'⛈️'};
  const desc={0:'Cerah',1:'Cerah berawan',2:'Berawan sebagian',3:'Berawan',45:'Berkabut',48:'Berkabut',51:'Gerimis ringan',53:'Gerimis',55:'Gerimis lebat',56:'Gerimis beku',57:'Gerimis beku',61:'Hujan ringan',63:'Hujan sedang',65:'Hujan lebat',66:'Hujan beku',67:'Hujan beku',71:'Salju ringan',73:'Salju',75:'Salju lebat',77:'Butiran salju',80:'Hujan lokal',81:'Hujan',82:'Hujan sangat lebat',85:'Salju lokal',86:'Salju',95:'Badai petir',96:'Petir + hujan es',99:'Petir + hujan es'};
  const dayName=['Min','Sen','Sel','Rab','Kam','Jum','Sab'];
  const fmtDate=(iso)=>{const d=new Date(iso+'T00:00:00+07:00');return dayName[d.getDay()]+' '+String(d.getDate()).padStart(2,'0')+'/'+String(d.getMonth()+1).padStart(2,'0')};
  const esc=(v)=>String(v).replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
  fetch(api,{headers:{'Accept':'application/json'}})
    .then(r=>{if(!r.ok) throw new Error('Open-Meteo proxy '+r.status);return r.json();})
    .then(data=>{
      const c=data.current||{};
      const code=c.weather_code ?? 0;
      const temp=c.temperature_2m;
      const rainNow=c.precipitation ?? 0;
      card.querySelector('[data-weather-icon]').textContent=iconMap[code]||'🌤️';
      card.querySelector('[data-weather-temp]').textContent=(temp==null?'—':Math.round(temp)+'°C');
      card.querySelector('[data-weather-desc]').textContent=(desc[code]||'Kondisi cuaca')+' · angin '+(c.wind_speed_10m==null?'—':Math.round(c.wind_speed_10m)+' km/j');
      const days=(data.daily?.time||[]).slice(0,5);
      const probs=(data.daily?.precipitation_probability_max||[]).slice(0,5);
      const tmax=(data.daily?.temperature_2m_max||[]).slice(0,5);
      const tmin=(data.daily?.temperature_2m_min||[]).slice(0,5);
      const codes=(data.daily?.weather_code||[]).slice(0,5);
      list.innerHTML=days.map((date,i)=>`<div class="forecast-item ${i===0?'today':''}"><div class="forecast-day">${i===0?'Hari ini':esc(fmtDate(date))}</div><div class="forecast-icon">${iconMap[codes[i]]||'🌤️'}</div><div class="forecast-temp">${Math.round(tmin[i])}° / ${Math.round(tmax[i])}°C</div><div class="forecast-rain">Hujan <strong>${probs[i]??0}%</strong></div></div>`).join('');
      const todayProb=probs[0]??0;
      card.querySelector('[data-weather-rain]').textContent=todayProb+'%';
    })
    .catch(()=>{
      card.querySelector('[data-weather-temp]').textContent='Tidak tersedia';
      card.querySelector('[data-weather-desc]').textContent='Periksa koneksi internet';
      list.innerHTML='<div class="forecast-loading">Data cuaca belum dapat dimuat. Silakan refresh halaman.</div>';
    });
})();
