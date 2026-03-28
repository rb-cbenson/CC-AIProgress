/* CC-AIProgress v0.4 — AI Intelligence Hub */

const S = { meta:null, cats:[], tools:[], news:[], regs:[], flows:[], tests:[], projects:[], strats:[], briefs:[], auto:{}, trustFramework:null,
  tab:'try-this', tf:{s:'',cat:'all',price:'all',trust:'all'}, nst:'sources', rf:'all', wst:'flows', cst:'',
  ts:{}, to:[], us:[], view:'compact' };

document.addEventListener('DOMContentLoaded', async()=>{
  loadState(); await loadData(); initRouter(); initSidebar(); initTheme(); initView(); initTips(); render();
});

// ===== DATA =====
async function loadData(){
  try{
    const b=basePath();
    const[m,c,t,n,r,w,x,p,st,br,au,tf]=await Promise.all(['meta','categories','tools','news-sources','regulations','workflows','tests','projects','strategies','briefings','automation','trust-framework'].map(f=>fetch(b+'data/'+f+'.json').then(r=>r.json()).catch(()=>[])));
    S.meta=m; S.cats=c; S.tools=t; S.news=n; S.regs=r; S.flows=w; S.tests=x; S.projects=p||[]; S.strats=st||[]; S.briefs=br||[]; S.auto=au||{pipelines:[],aiAccounts:[],automationGoals:[]}; S.trustFramework=tf||null;
    if(!S.to.length) S.to=x.map(t=>t.id);
    updFoot();
  }catch(e){
    document.querySelector('.main-content').innerHTML=`<div style="text-align:center;padding:40px;color:var(--text-muted)"><h3>Load error</h3><p>${e.message}</p><p>Try: <code>python -m http.server 8000</code></p></div>`;
  }
}
function basePath(){ const p=location.pathname; return p.endsWith('.html')||p.endsWith('/')?p.substring(0,p.lastIndexOf('/')+1):p+'/'; }

// ===== STATE =====
function loadState(){ try{ const d=JSON.parse(localStorage.getItem('ai-dash')||'{}'); S.ts=d.ts||{}; S.to=d.to||[]; S.us=d.us||[]; }catch(e){} }
function save(){ localStorage.setItem('ai-dash',JSON.stringify({ts:S.ts,to:S.to,us:S.us})); }
function gts(id){ return S.ts[id]||''; }
function sts(id,v){ if(v)S.ts[id]=v; else delete S.ts[id]; save(); renderTests(); }

// ===== ROUTING =====
function initRouter(){ window.addEventListener('hashchange',()=>{ S.tab=location.hash.slice(1)||'command-center'; render(); updNav(); }); S.tab=location.hash.slice(1)||'command-center'; updNav(); }
function updNav(){ document.querySelectorAll('.sidebar-nav a').forEach(a=>a.classList.toggle('active',a.getAttribute('href')==='#'+S.tab)); }
function nav(t){ location.hash=t; }

// ===== SIDEBAR / THEME / VIEW =====
function initSidebar(){ const t=document.querySelector('.sidebar-toggle'),s=document.querySelector('.sidebar'); if(t){t.onclick=()=>s.classList.toggle('open'); s.querySelectorAll('.sidebar-nav a').forEach(a=>a.onclick=()=>s.classList.remove('open'));} }
function initTheme(){ const s=localStorage.getItem('ai-dash-theme'); if(s)document.documentElement.setAttribute('data-theme',s); const b=document.getElementById('theme-toggle-btn'); if(b){b.onclick=()=>{const n=document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark'; document.documentElement.setAttribute('data-theme',n); localStorage.setItem('ai-dash-theme',n); b.textContent=n==='dark'?'☀ Light':'🌙 Dark';}; b.textContent=document.documentElement.getAttribute('data-theme')==='dark'?'☀ Light':'🌙 Dark';} }
function initView(){ const s=localStorage.getItem('ai-dash-view')||'compact'; S.view=s; document.documentElement.setAttribute('data-view',s); document.querySelectorAll('.view-btn').forEach(b=>{b.classList.toggle('active',b.dataset.view===s); b.onclick=()=>{S.view=b.dataset.view; document.documentElement.setAttribute('data-view',b.dataset.view); localStorage.setItem('ai-dash-view',b.dataset.view); document.querySelectorAll('.view-btn').forEach(x=>x.classList.toggle('active',x===b));};}); }
function initTips(){ const tip=document.getElementById('tooltip'); let tm; document.addEventListener('mouseover',e=>{const el=e.target.closest('[data-tip]'); if(!el)return; clearTimeout(tm); tm=setTimeout(()=>{tip.textContent=el.dataset.tip; const r=el.getBoundingClientRect(); tip.style.left=Math.min(r.left,innerWidth-320)+'px'; tip.style.top=(r.bottom+4)+'px'; tip.classList.add('visible');},350);}); document.addEventListener('mouseout',e=>{if(e.target.closest('[data-tip]')){clearTimeout(tm);tip.classList.remove('visible');}}); }

// ===== RENDER =====
function render(){ document.querySelectorAll('.tab-content').forEach(t=>t.classList.remove('active')); const el=document.getElementById('tab-'+S.tab); if(el){el.classList.add('active'); ({
  'command-center':renderCommandCenter, 'try-this':renderTests, tools:renderTools, news:renderNews, rankings:renderRankings, workflows:renderFlows, strategies:renderStrategies, about:renderAbout
})[S.tab]?.();} }

// Helpers
function cat(t){ return S.cats.find(c=>c.id===t.category)||{color:'#999',name:t.category,description:''}; }
function logo(t,c){ try{const d=new URL(t.url).hostname; return `<img class="tc-logo" src="https://www.google.com/s2/favicons?domain=${d}&sz=64" alt="" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'"><div class="tc-avatar" style="background:${c.color};display:none">${t.name[0]}</div>`;}catch(e){return `<div class="tc-avatar" style="background:${c.color}">${t.name[0]}</div>`;} }
function esc(s){ return (s||'').replace(/"/g,'&quot;').replace(/</g,'&lt;'); }
function days(d){ return Math.floor((Date.now()-new Date(d).getTime())/864e5); }
function linkify(t){ return t.replace(/(https?:\/\/[^\s,)]+)/g,'<a href="$1" target="_blank">$1</a>').replace(/\b(Go to|Visit)\s+([a-z]+\.[a-z.]+)/gi,'$1 <a href="https://$2" target="_blank">$2</a>'); }
function catCount(id){ return S.tools.filter(t=>t.category===id).length; }
const ICONS={'message-circle':'💬','photo':'🖼️','video':'🎬','music':'🎵','code':'💻','clipboard':'📋','3d-cube-sphere':'🧊','layers-intersect':'🔗','arrows-shuffle':'⚡','robot':'🤖','server':'🖥️','shield-check':'🛡️','microphone':'🎙️','chart-bar':'📊'};
function catIcon(c){ return ICONS[c.icon]||'📦'; }

// ===== TRUST SCORE =====
// HYBRID: Blends static baseline (from tools.json, set by research/incidents) with
// dynamic signals (ranking, trend, freshness, pros/cons). Neither alone is sufficient:
// - Static catches security incidents, scams, known issues (can't compute these)
// - Dynamic catches staleness, ranking drift, trend changes (auto-updates)
// If a tool has a known incident in trust-framework.json, that overrides upward.
function trustScore(t){
  // Dynamic component (0-100 range, computed from live data signals)
  let dynamic=50;
  const totalTools=S.tools.length||1;
  const rankPct=1-(t.ranking.overall-1)/(totalTools-1||1);
  dynamic+=rankPct*20; // max ~20 pts from ranking
  if(t.ranking.trend==='rising') dynamic+=8;
  else if(t.ranking.trend==='stable') dynamic+=4;
  else if(t.ranking.trend==='declining') dynamic-=8;
  const prosLen=t.pros?t.pros.length:0, consLen=t.cons?t.cons.length:0;
  if(prosLen+consLen>0) dynamic+=((prosLen-consLen)/(prosLen+consLen))*8;
  const staleDays=days(t.lastVerified);
  if(staleDays<=30) dynamic+=8;
  else if(staleDays<=90) dynamic+=4;
  else if(staleDays>180) dynamic-=8;
  if(t.pricingCAD.freeTier) dynamic+=4;
  dynamic=Math.max(0,Math.min(100,Math.round(dynamic)));

  // Static baseline (from tools.json, set by research — captures security incidents, reputation)
  const baseline=typeof t.trustScore==='number'?t.trustScore:null;

  // Blend: if baseline exists, weight it 40% static / 60% dynamic
  // If no baseline, use 100% dynamic (new tools start computed-only)
  let final;
  if(baseline!==null) final=Math.round(baseline*0.4+dynamic*0.6);
  else final=dynamic;

  // Check trust-framework known incidents (loaded into S.trustFramework if available)
  if(S.trustFramework&&S.trustFramework.knownIncidents){
    const incident=S.trustFramework.knownIncidents.find(i=>i.tool===t.id);
    if(incident){
      // Active incidents cap the score based on severity
      if(incident.status!=='resolved'){
        if(incident.severity==='critical') final=Math.min(final,40);
        else if(incident.severity==='high') final=Math.min(final,55);
        else if(incident.severity==='medium') final=Math.min(final,70);
      }
    }
  }

  return Math.max(0,Math.min(100,final));
}

function trustTier(score){
  if(score>=80) return {label:'TRUSTED',cls:'trust-trusted',color:'#06d6a0'};
  if(score>=60) return {label:'CAUTION',cls:'trust-caution',color:'#ffd166'};
  if(score>=40) return {label:'ELEVATED RISK',cls:'trust-elevated',color:'#ef476f'};
  if(score>=20) return {label:'HIGH RISK',cls:'trust-high',color:'#d00000'};
  return {label:'AVOID',cls:'trust-avoid',color:'#1a1a2e'};
}

function trustBadgeHtml(t){
  const sc=trustScore(t), tier=trustTier(sc);
  return `<span class="b trust-badge ${tier.cls}" style="background:${tier.color};color:${sc>=60&&sc<80?'#333':'#fff'};font-weight:700;font-size:9px;letter-spacing:0.5px;cursor:pointer" onclick="event.stopPropagation();showTrustDetail('${t.id}')" data-tip="Click for trust breakdown">${tier.label} (${sc})</span>`;
}

function trustBreakdown(t){
  // Recompute each component for transparency
  const totalTools=S.tools.length||1;
  const rankPct=1-(t.ranking.overall-1)/(totalTools-1||1);
  const rankPts=Math.round(rankPct*20);
  const trendPts=t.ranking.trend==='rising'?8:t.ranking.trend==='stable'?4:-8;
  const prosLen=t.pros?t.pros.length:0, consLen=t.cons?t.cons.length:0;
  const pcPts=(prosLen+consLen>0)?Math.round(((prosLen-consLen)/(prosLen+consLen))*8):0;
  const staleDays=days(t.lastVerified);
  const freshPts=staleDays<=30?8:staleDays<=90?4:staleDays>180?-8:0;
  const freePts=t.pricingCAD.freeTier?4:0;
  const dynamic=Math.max(0,Math.min(100,50+rankPts+trendPts+pcPts+freshPts+freePts));
  const baseline=typeof t.trustScore==='number'?t.trustScore:null;
  let final=baseline!==null?Math.round(baseline*0.4+dynamic*0.6):dynamic;
  let incident=null;
  let capped=false;
  if(S.trustFramework&&S.trustFramework.knownIncidents){
    incident=S.trustFramework.knownIncidents.find(i=>i.tool===t.id);
    if(incident&&incident.status!=='resolved'){
      const cap=incident.severity==='critical'?40:incident.severity==='high'?55:70;
      if(final>cap){capped=true;final=cap;}
    }
  }
  return {rankPts,trendPts,pcPts,freshPts,freePts,dynamic,baseline,final,incident,capped,staleDays,prosLen,consLen};
}

function showTrustDetail(toolId){
  const t=S.tools.find(x=>x.id===toolId);
  if(!t)return;
  const b=trustBreakdown(t);
  const tier=trustTier(b.final);
  const old=document.getElementById('trust-modal');
  if(old)old.remove();

  const bar=(label,pts,max,color)=>{
    const pct=Math.max(0,Math.min(100,((pts+max)/(max*2))*100));
    return `<div style="display:flex;align-items:center;gap:8px;margin:3px 0">
      <span style="width:120px;font-size:11px;color:var(--text-muted)">${label}</span>
      <div style="flex:1;height:8px;background:var(--border);border-radius:4px;overflow:hidden">
        <div style="width:${pct}%;height:100%;background:${color};border-radius:4px;transition:width .3s"></div>
      </div>
      <span style="width:35px;text-align:right;font-size:11px;font-weight:600;color:${pts>=0?'var(--success)':'var(--danger)'}">${pts>=0?'+':''}${pts}</span>
    </div>`;
  };

  const modal=document.createElement('div');
  modal.id='trust-modal';
  modal.style.cssText='position:fixed;inset:0;z-index:9999;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,0.5);backdrop-filter:blur(3px)';
  modal.onclick=e=>{if(e.target===modal)modal.remove();};

  modal.innerHTML=`
    <div style="background:var(--card-bg,#fff);border-radius:12px;padding:24px;max-width:480px;width:90%;max-height:85vh;overflow-y:auto;box-shadow:0 20px 60px rgba(0,0,0,0.3)">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
        <h3 style="margin:0;font-size:16px">${t.name} — Trust Score</h3>
        <button onclick="document.getElementById('trust-modal').remove()" style="background:none;border:none;font-size:20px;cursor:pointer;color:var(--text-muted);padding:0">✕</button>
      </div>

      <div style="text-align:center;margin-bottom:16px">
        <div style="display:inline-block;width:80px;height:80px;border-radius:50%;background:${tier.color};color:${b.final>=60&&b.final<80?'#333':'#fff'};line-height:80px;font-size:28px;font-weight:800">${b.final}</div>
        <div style="margin-top:6px;font-weight:700;color:${tier.color}">${tier.label}</div>
      </div>

      <div style="background:var(--bg-subtle,#f8f9fa);border-radius:8px;padding:12px;margin-bottom:12px">
        <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--text-muted);margin-bottom:8px">Dynamic Signals (60% weight)</div>
        ${bar('Ranking (#'+t.ranking.overall+')',b.rankPts,20,'#4361ee')}
        ${bar('Trend ('+t.ranking.trend+')',b.trendPts,8,b.trendPts>=0?'#06d6a0':'#ef476f')}
        ${bar('Pros vs Cons ('+b.prosLen+'/'+b.consLen+')',b.pcPts,8,b.pcPts>=0?'#06d6a0':'#ef476f')}
        ${bar('Data Freshness ('+b.staleDays+'d)',b.freshPts,8,b.freshPts>=0?'#06d6a0':'#ef476f')}
        ${bar('Free Tier',b.freePts,4,b.freePts>0?'#06d6a0':'#999')}
        <div style="text-align:right;font-size:12px;margin-top:6px;font-weight:600">Dynamic: ${b.dynamic}/100</div>
      </div>

      <div style="background:var(--bg-subtle,#f8f9fa);border-radius:8px;padding:12px;margin-bottom:12px">
        <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--text-muted);margin-bottom:4px">Research Baseline (40% weight)</div>
        <div style="font-size:13px">${b.baseline!==null?`<strong>${b.baseline}/100</strong> — set by AI research based on company reputation, security track record, adoption`:'<em style="color:var(--text-muted)">No baseline set — using 100% dynamic score</em>'}</div>
      </div>

      ${b.incident?`
      <div style="background:${b.capped?'rgba(239,71,111,0.1)':'rgba(6,214,160,0.1)'};border:1px solid ${b.capped?'#ef476f':'#06d6a0'};border-radius:8px;padding:12px;margin-bottom:12px">
        <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:${b.capped?'#ef476f':'#06d6a0'};margin-bottom:4px">
          ${b.capped?'⚠ SECURITY INCIDENT — SCORE CAPPED':'Security Incident (Resolved)'}
        </div>
        <div style="font-size:12px"><strong>${b.incident.type}</strong> (${b.incident.severity}) — ${b.incident.date}</div>
        <div style="font-size:11px;color:var(--text-muted);margin-top:4px">${b.incident.description}</div>
        <div style="font-size:11px;margin-top:4px">Status: <strong>${b.incident.status}</strong></div>
      </div>`:''}

      <div style="font-size:10px;color:var(--text-muted);line-height:1.5;border-top:1px solid var(--border);padding-top:10px">
        <strong>How this works:</strong> Score blends a research-set baseline (company reputation, security history) with live signals (ranking, trend, data freshness). Known security incidents can cap scores regardless of other factors. Scores update automatically as data changes — no manual intervention needed.
        <br><br>Last verified: ${t.lastVerified}
      </div>
    </div>`;

  document.body.appendChild(modal);
}

function trustDistribution(){
  const dist={trusted:0,caution:0,elevated:0,high:0,avoid:0};
  S.tools.forEach(t=>{
    const sc=trustScore(t);
    if(sc>=80) dist.trusted++;
    else if(sc>=60) dist.caution++;
    else if(sc>=40) dist.elevated++;
    else if(sc>=20) dist.high++;
    else dist.avoid++;
  });
  return dist;
}

// ===== TRY THIS (LANDING) =====
function renderTests(){
  const el=document.getElementById('tab-try-this');
  const ord=getOrd(), act=ord.filter(t=>gts(t.id)!=='deleted'&&gts(t.id)!=='tried');
  const saved=ord.filter(t=>gts(t.id)==='saved'), tried=ord.filter(t=>gts(t.id)==='tried');
  const asap=act.filter(t=>t.priority==='try-asap'&&gts(t.id)!=='saved');
  const rec=act.filter(t=>t.priority==='recommended'&&gts(t.id)!=='saved');
  const opt=act.filter(t=>t.priority==='optional'&&gts(t.id)!=='saved');
  const free=S.tools.filter(t=>t.pricingCAD.freeTier).length;
  const rising=S.tools.filter(t=>t.ranking.trend==='rising').length;
  const topTool=S.tools.reduce((a,b)=>a.ranking.overall<b.ranking.overall?a:b,S.tools[0]);
  const newestCat=S.cats.reduce((a,b)=>catCount(b.id)>catCount(a.id)?b:a,S.cats[0]);

  el.innerHTML=`
    <div class="section-banner" data-ai-section="overview" data-ai-description="Dashboard landing page with AI tool intelligence summary">
      <h2>AI Intelligence Hub</h2>
      <p>Your AI assistant for AI guidance, testing & development — amassing intelligence about everything AI</p>
      <div class="banner-stats">
        <span>${S.tools.length} tools tracked</span>
        <span>${free} free tiers</span>
        <span>${rising} rising</span>
        <span>${S.news.length + S.regs.length} intelligence sources</span>
        <span>${S.flows.length} workflows</span>
        <span>${tried.length}/${S.tests.length} tests done</span>
      </div>
      <div class="banner-stats" style="margin-top:4px">
        ${(()=>{const d=trustDistribution(); return `
        <span style="color:#06d6a0">🛡️ ${d.trusted} trusted</span>
        <span style="color:#ffd166">⚠ ${d.caution} caution</span>
        <span style="color:#ef476f">🚨 ${d.elevated} elevated risk</span>
        ${d.high?`<span style="color:#d00000">${d.high} high risk</span>`:''}
        ${d.avoid?`<span style="color:#1a1a2e">${d.avoid} avoid</span>`:''}`;})()}
      </div>
    </div>

    <div class="stats">
      <div class="stat" onclick="nav('tools')" data-tip="Browse all ${S.tools.length} tools with search/filters">
        <b>${S.tools.length}</b><span>Tools Indexed</span>
      </div>
      <div class="stat" onclick="nav('tools');setTimeout(()=>{S.tf.price='free';renderTools()},50)" data-tip="Usable right now — no credit card needed">
        <b style="color:var(--success)">${free}</b><span>Free Tier</span>
      </div>
      <div class="stat" onclick="nav('rankings')" data-tip="Tools with strong growth trajectory">
        <b style="color:var(--primary)">${rising}</b><span>Rising Fast</span>
      </div>
      <div class="stat" onclick="nav('news')" data-tip="News, regulations, research feeds">
        <b>${S.news.length + S.regs.length}</b><span>Intel Sources</span>
      </div>
      <div class="stat" data-tip="#1 ranked overall: ${topTool?.name}">
        <b style="font-size:14px">${topTool?.name||'—'}</b><span>#1 Overall</span>
      </div>
      <div class="stat" onclick="nav('tools');setTimeout(()=>{S.tf.trust='trusted';renderTools()},50)" data-tip="Tools scoring 80+ trust score">
        <b style="color:#06d6a0">${trustDistribution().trusted}</b><span>Trusted</span>
      </div>
    </div>

    <div class="cat-strip" data-ai-section="categories" data-ai-description="Category distribution overview">
      ${S.cats.map(c=>`<div class="cat-chip" onclick="nav('tools');setTimeout(()=>{S.tf.cat='${c.id}';renderTools()},50)" data-tip="${c.description}">
        <span class="cc-dot" style="background:${c.color}"></span>
        <span>${c.name}</span>
        <span class="cc-count">${catCount(c.id)}</span>
      </div>`).join('')}
    </div>

    ${saved.length?`<div class="sh"><h3>📌 Saved for Later (${saved.length})</h3></div>${saved.map(testCard).join('')}`:''}
    ${asap.length?`<div class="sh"><h3 style="color:var(--success)">⚡ Try ASAP — High Impact</h3><p>These represent the fastest-moving areas of AI right now. Testing them gives you hands-on understanding that reading about them can't.</p></div>${asap.map(testCard).join('')}`:''}
    ${rec.length?`<div class="sh"><h3 style="color:var(--primary)">👍 Recommended</h3><p>Solid practical value — useful tools you'll come back to.</p></div>${rec.map(testCard).join('')}`:''}
    ${opt.length?`<div class="sh"><h3>Optional — Nice to Know</h3></div>${opt.map(testCard).join('')}`:''}
    ${tried.length?`<div class="sh"><h3>✓ Completed (${tried.length})</h3></div>${tried.map(testCard).join('')}`:''}

    <div class="card" style="margin-top:12px;background:var(--primary-soft);border-color:var(--primary)" data-ai-section="ai-capabilities" data-ai-description="What this system can do with AI assistance">
      <h3 style="margin:0 0 6px;font-size:14px;color:var(--primary)">🤖 What This System Can Do</h3>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px;font-size:var(--font-xs)">
        <div><strong>Now (Standalone)</strong>
          <ul style="margin:4px 0;padding-left:16px;color:var(--text-muted)">
            <li>Track ${S.tools.length} AI tools across ${S.cats.length} categories</li>
            <li>Compare pricing, features, rankings</li>
            <li>Step-by-step testing guides</li>
            <li>Regulation tracking (${S.regs.length} policies)</li>
            <li>Workflow pipelines for tool combinations</li>
          </ul>
        </div>
        <div><strong>Now (With AI)</strong>
          <ul style="margin:4px 0;padding-left:16px;color:var(--text-muted)">
            <li>Daily research: new tools, pricing changes, shutdowns</li>
            <li>Verify data accuracy via web search</li>
            <li>Generate new tests when tools launch</li>
            <li>Review user-submitted URLs for relevance</li>
            <li>Summarize AI news across all sources</li>
          </ul>
        </div>
        <div><strong>Coming (AI + Automation)</strong>
          <ul style="margin:4px 0;padding-left:16px;color:var(--text-muted)">
            <li>Auto-open tools in browser for testing</li>
            <li>Run comparison benchmarks automatically</li>
            <li>Detect AI-generated misinformation</li>
            <li>Predict which tools will dominate next</li>
            <li>Custom code to overcome any obstacle</li>
          </ul>
        </div>
      </div>
      <p style="margin:6px 0 0;font-size:10px;color:var(--text-muted)">Nothing is a brick wall — anything can be overcome. This list grows as we discover what's possible.</p>
    </div>`;
  initDrag();
}

function getOrd(){ return [...S.tests].sort((a,b)=>{const ai=S.to.indexOf(a.id),bi=S.to.indexOf(b.id); if(ai===-1&&bi===-1)return 0; if(ai===-1)return 1; if(bi===-1)return -1; return ai-bi;}); }

const WHY={
  'video-generation':'Video AI evolves fastest — Sora shut down March 2026 and competitors already surpassed it. See what\'s actually possible now.',
  'text-chat':'Chat AI is the most broadly useful category. Finding YOUR preferred tool saves time on everything.',
  'audio-music':'AI music went from novelty to professional-grade in months. Create real songs with zero training.',
  'coding-assistants':'AI coding is the fastest-growing dev tool category. Even non-developers can build working software.',
  'image-generation':'Free image AI improved dramatically — understand the quality gap to budget wisely.',
  'productivity':'These replace hours of manual work. The research workflow alone could change how you learn.',
  'workflow-automation':'Automation compounds — one Zap saves minutes daily, hours monthly.',
  'all-in-one':'Local AI = complete privacy, zero ongoing cost. Worth knowing even if you prefer cloud.'
};

function testCard(t){
  const ts=gts(t.id), sc=ts?' user-'+ts:'';
  const tools=t.toolsNeeded.map(tn=>{const tl=S.tools.find(x=>x.id===tn.toolId); return `<a href="${tl?tl.url:'#'}" target="_blank">${tl?tl.name:tn.toolId}</a> — ${tn.role}`;}).join(' · ');
  return `<div class="card test p-${t.priority}${sc}" id="test-${t.id}" draggable="true" data-test-id="${t.id}"
    data-ai-test="${t.id}" data-ai-category="${t.category}" data-ai-priority="${t.priority}" data-ai-status="${ts||'pending'}">
    <div class="test-head"><h3><span class="drag-handle">⠿</span> ${t.title}</h3>
      ${ts==='tried'?'<span style="color:var(--success);font-size:11px;font-weight:700">✓ Done</span>':''}${ts==='saved'?'<span style="color:#92400e;font-size:11px">📌 Saved</span>':''}</div>
    <div class="test-tags"><span class="b b-priority ${t.priority}">${t.priority.replace(/-/g,' ')}</span> <span class="b" style="background:var(--bg);color:var(--text-muted)">${t.difficulty}</span> <span class="b" style="background:var(--bg);color:var(--text-muted)">${t.timeEstimate}</span> <span class="b-standalone">Standalone</span></div>
    <div style="font-size:var(--font-xs);color:var(--text-muted);margin-bottom:4px">${t.description}</div>
    <div class="test-why">${WHY[t.category]||'Hands-on experience beats reading about it.'}</div>
    <div class="test-tools">${tools}${t.hardwareNeeded.length?' · <span style="color:var(--text-muted)">Needs: '+t.hardwareNeeded.join(', ')+'</span>':''}</div>
    <div class="test-actions">
      <button class="btn btn-x" onclick="toggleSteps('${t.id}')">▶ Steps</button>
      ${ts!=='tried'?`<button class="btn btn-s" onclick="sts('${t.id}','tried')">✓ Done</button>`:`<button class="btn btn-o" onclick="sts('${t.id}','')">↩ Undo</button>`}
      ${ts!=='saved'?`<button class="btn btn-save" onclick="sts('${t.id}','saved')" data-tip="Save for later — AI tracks if something better emerges">📌 Later</button>`:`<button class="btn btn-o" onclick="sts('${t.id}','')">↩ Undo</button>`}
      <button class="btn btn-d" onclick="sts('${t.id}','deleted')" data-tip="Remove from list">✕</button>
    </div>
    <div class="test-steps" id="steps-${t.id}">${t.steps.map(s=>`<div class="test-step"><b>Step ${s.step}: ${s.title}</b><p>${linkify(s.instructions)}</p>${s.tip?`<p class="tip">💡 ${s.tip}</p>`:''}</div>`).join('')}
      <div class="card" style="margin-top:6px;background:var(--bg)"><b style="font-size:var(--font-xs)">Expected Result:</b> <span style="font-size:var(--font-xs);color:var(--text-muted)">${t.expectedOutcome}</span></div>
    </div></div>`;
}

function toggleSteps(id){ const s=document.getElementById('steps-'+id); if(s){s.classList.toggle('open'); const b=s.previousElementSibling.querySelector('.btn-x'); if(b)b.textContent=s.classList.contains('open')?'▼ Hide Steps':'▶ Steps';} }

function initDrag(){ let did; document.querySelectorAll('.test[draggable]').forEach(c=>{
  c.ondragstart=()=>{did=c.dataset.testId;c.classList.add('dragging')};
  c.ondragend=()=>{c.classList.remove('dragging');document.querySelectorAll('.drag-over').forEach(x=>x.classList.remove('drag-over'))};
  c.ondragover=e=>{e.preventDefault();c.classList.add('drag-over')};
  c.ondragleave=()=>c.classList.remove('drag-over');
  c.ondrop=e=>{e.preventDefault();c.classList.remove('drag-over');const tid=c.dataset.testId;if(did&&tid&&did!==tid){const o=[...S.to],f=o.indexOf(did),t=o.indexOf(tid);if(f>-1&&t>-1){o.splice(f,1);o.splice(t,0,did);S.to=o;save();renderTests();}}}
});}

// ===== TOOLS =====
function renderTools(){
  const el=document.getElementById('tab-tools');
  const free=S.tools.filter(t=>t.pricingCAD.freeTier).length;
  const rising=S.tools.filter(t=>t.ranking.trend==='rising').length;
  const catPills=S.cats.map(c=>`<span class="pill${S.tf.cat===c.id?' on':''}" onclick="S.tf.cat='${c.id}';renderTools()" data-tip="${c.description} (${catCount(c.id)} tools)"><span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:${c.color};margin-right:3px"></span>${c.name}</span>`).join('');

  el.innerHTML=`
    <div class="section-banner" data-ai-section="tools-database" data-ai-description="Complete AI tools database with ${S.tools.length} tools across ${S.cats.length} categories">
      <h2>AI Tools Database</h2>
      <p>${S.tools.length} tools · ${S.cats.length} categories · All pricing in CAD ($1 USD ≈ $${S.meta?.cadExchangeRate} CAD)</p>
      <div class="banner-stats">
        <span>${free} free tiers</span>
        <span>${rising} rising</span>
        <span>${S.tools.length - free} paid only</span>
        <span>Updated ${S.meta?.lastUpdated}</span>
      </div>
    </div>
    <input class="search" placeholder="Search tools, developers, features, categories..." value="${S.tf.s}" oninput="S.tf.s=this.value;fillTools()">
    <div class="pills">
      <span class="pill${S.tf.cat==='all'?' on':''}" onclick="S.tf.cat='all';renderTools()">All (${S.tools.length})</span>${catPills}
    </div>
    <div class="pills">
      <span class="pill${S.tf.price==='all'?' on':''}" onclick="S.tf.price='all';renderTools()">All Pricing</span>
      <span class="pill${S.tf.price==='free'?' on':''}" onclick="S.tf.price='free';renderTools()">Free Tier (${free})</span>
      <span class="pill${S.tf.price==='paid'?' on':''}" onclick="S.tf.price='paid';renderTools()">Paid Only (${S.tools.length - free})</span>
    </div>
    <div class="pills">
      ${(()=>{const d=trustDistribution(); return `
      <span class="pill${S.tf.trust==='all'?' on':''}" onclick="S.tf.trust='all';renderTools()">All Trust Levels</span>
      <span class="pill${S.tf.trust==='trusted'?' on':''}" onclick="S.tf.trust='trusted';renderTools()" style="border-color:#06d6a0">🛡️ Trusted (${d.trusted})</span>
      <span class="pill${S.tf.trust==='caution'?' on':''}" onclick="S.tf.trust='caution';renderTools()" style="border-color:#ffd166">⚠ Caution (${d.caution})</span>
      <span class="pill${S.tf.trust==='atrisk'?' on':''}" onclick="S.tf.trust='atrisk';renderTools()" style="border-color:#ef476f">🚨 At Risk (${d.elevated+d.high+d.avoid})</span>`;})()}
    </div>
    <div class="grid grid-2" id="tgrid"></div>`;
  fillTools();
}

function fillTools(){
  let t=[...S.tools]; const{s,cat:c,price:p,trust:tr}=S.tf;
  if(s){const q=s.toLowerCase();t=t.filter(x=>x.name.toLowerCase().includes(q)||x.developer.toLowerCase().includes(q)||x.description.toLowerCase().includes(q)||x.category.includes(q));}
  if(c!=='all')t=t.filter(x=>x.category===c);
  if(p==='free')t=t.filter(x=>x.pricingCAD.freeTier);
  if(p==='paid')t=t.filter(x=>!x.pricingCAD.freeTier);
  if(tr==='trusted')t=t.filter(x=>trustScore(x)>=80);
  else if(tr==='caution')t=t.filter(x=>{const sc=trustScore(x);return sc>=60&&sc<80;});
  else if(tr==='atrisk')t=t.filter(x=>trustScore(x)<60);
  t.sort((a,b)=>a.ranking.overall-b.ranking.overall);
  const g=document.getElementById('tgrid');
  if(g) g.innerHTML=t.length?t.map(toolCard).join(''):`<div style="text-align:center;padding:30px;color:var(--text-muted);grid-column:1/-1"><p>No tools match "${S.tf.s}" — try different keywords</p></div>`;
}

function toolCard(t){
  const c=cat(t);
  const ps=t.pricingCAD.freeTier?`<strong>Free</strong>${t.pricingCAD.paidPlans.length?' · from $'+Math.min(...t.pricingCAD.paidPlans.map(p=>p.priceCAD))+'/'+t.pricingCAD.paidPlans[0].period:''}`:t.pricingCAD.paidPlans.length?`From <strong>$${Math.min(...t.pricingCAD.paidPlans.map(p=>p.priceCAD))}</strong>/${t.pricingCAD.paidPlans[0].period}`:'Contact';
  const rows=t.pricingCAD.paidPlans.map(p=>`<tr><td>${p.name}</td><td><strong>$${p.priceCAD}</strong>/${p.period}</td><td>${p.details}</td></tr>`).join('');
  const stale=days(t.lastVerified)>90;
  return `<div class="card tc" style="border-top-color:${c.color}"
    data-tip="${t.developer} · #${t.ranking.overall} overall · ${t.ranking.trend}"
    data-ai-tool="${t.id}" data-ai-category="${t.category}" data-ai-rank="${t.ranking.overall}" data-ai-trend="${t.ranking.trend}" data-ai-free="${t.pricingCAD.freeTier}" data-ai-trust="${trustScore(t)}">
    <div class="tc-rank">#${t.ranking.overall}</div>
    <div class="tc-head">${logo(t,c)}<div class="tc-info"><h4 class="tc-name"><a href="${t.url}" target="_blank">${t.name}</a></h4><div class="tc-dev">${t.developer}</div></div></div>
    <div class="tc-desc">${t.description}</div>
    <div class="tc-tags"><span class="b b-cat" style="background:${c.color}">${c.name}</span> ${t.pricingCAD.freeTier?'<span class="b b-free" data-tip="'+esc(t.pricingCAD.freeTierDetails)+'">Free</span>':'<span class="b b-paid">Paid</span>'} <span class="b b-trend ${t.ranking.trend}">${t.ranking.trend}</span> ${trustBadgeHtml(t)}${stale?' <span class="b" style="background:rgba(255,209,102,0.2);color:#92400e" data-tip="Data may be outdated — last checked '+t.lastVerified+'">⚠ verify</span>':''}</div>
    <div class="tc-price">${ps}</div>
    <button class="tc-expand" onclick="togDet('${t.id}')">▶ Details & pricing</button>
    <div class="tc-details" id="det-${t.id}">
      ${t.pricingCAD.freeTier?`<h5>Free Tier</h5><p style="color:var(--text-muted)">${t.pricingCAD.freeTierDetails}</p>`:''}
      ${rows?`<h5>Plans (CAD)</h5><table><tr><th>Plan</th><th>Price</th><th>Details</th></tr>${rows}</table>`:''}
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:6px">
        <div><h5 style="color:var(--success)">✓ Pros</h5><ul>${t.pros.map(p=>'<li>'+p+'</li>').join('')}</ul></div>
        <div><h5 style="color:var(--danger)">✕ Cons</h5><ul>${t.cons.map(c=>'<li>'+c+'</li>').join('')}</ul></div>
      </div>
      <div style="color:var(--text-muted);margin-top:6px;font-size:10px">Verified: ${t.lastVerified} <span class="b-ai">AI-verified</span></div>
    </div></div>`;
}

function togDet(id){const d=document.getElementById('det-'+id);if(d){d.classList.toggle('open');const b=d.previousElementSibling;if(b)b.textContent=d.classList.contains('open')?'▼ Hide details':'▶ Details & pricing';}}

// ===== AI NEWS & INTELLIGENCE =====
function renderNews(){
  const el=document.getElementById('tab-news');
  el.innerHTML=`
    <div class="section-banner" data-ai-section="intelligence" data-ai-description="AI news intelligence feeds, regulation tracking, and user-curated sources">
      <h2>AI Intelligence Feed</h2>
      <p>News, research, regulations, and your custom sources — the research backbone of staying current</p>
      <div class="banner-stats">
        <span>${S.news.length} curated sources</span>
        <span>${S.regs.length} regulations tracked</span>
        <span>${S.us.length} your sources</span>
        <span>${S.news.filter(s=>s.free).length} free</span>
      </div>
    </div>
    <div class="stabs">
      <button class="stab${S.nst==='sources'?' active':''}" onclick="S.nst='sources';fillNews()">📡 Sources (${S.news.length})</button>
      <button class="stab${S.nst==='regs'?' active':''}" onclick="S.nst='regs';fillNews()">⚖️ Regulations (${S.regs.length})</button>
      <button class="stab${S.nst==='landscape'?' active':''}" onclick="S.nst='landscape';fillNews()">🗺️ Landscape</button>
      <button class="stab${S.nst==='add'?' active':''}" onclick="S.nst='add';fillNews()">+ Add Source</button>
    </div>
    <div id="ncontent"></div>`;
  fillNews();
}

function fillNews(){
  const el=document.getElementById('ncontent'); if(!el)return;

  if(S.nst==='sources'){
    const types=[
      {k:'newsletter',l:'📨 Newsletters',d:'The fastest way to stay current — subscribe to 2-3 and you\'ll catch 90% of major AI news'},
      {k:'youtube',l:'🎬 YouTube',d:'Visual explainers and demos — seeing AI in action is different from reading about it'},
      {k:'news-site',l:'📰 News Sites',d:'In-depth analysis and breaking stories'},
      {k:'blog',l:'✍️ Blogs & Writers',d:'Deep dives from practitioners and researchers — often the most insightful analysis'},
      {k:'podcast',l:'🎙️ Podcasts',d:'Long-form AI discussion — listen while commuting or working'},
      {k:'reddit',l:'💬 Reddit Communities',d:'Real-time community discussion — often first to spot new tools and issues'},
      {k:'discord',l:'🎮 Discord Servers',d:'Direct access to tool communities, beta testing, and developer discussions'},
      {k:'community',l:'🌐 Communities',d:'Forums, Slack groups, and other gathering places for AI practitioners'},
      {k:'directory',l:'📂 Tool Directories',d:'Discover tools these databases track that we don\'t — yet'},
      {k:'research',l:'🔬 Research & Academic',d:'Papers, preprints, and academic resources — where breakthroughs appear first'},
      {k:'api-source',l:'🔌 APIs & Programmatic',d:'Machine-readable feeds for automated discovery — the backbone of our tracking system'},
      {k:'github',l:'🐙 GitHub',d:'Open-source projects, trending repos, and code-level AI developments'},
      {k:'twitter-list',l:'🐦 Twitter/X Lists',d:'Curated feeds from AI researchers, founders, and practitioners'},
      {k:'rss',l:'📡 RSS & Aggregators',d:'Combine multiple feeds into one stream'},
      {k:'regulation',l:'🇨🇦 AI Policy & Regulation',d:'Government sources for AI regulation — directly affects what tools can do here'}
    ];
    const userHtml=S.us.length?`<div class="sh" style="margin-bottom:6px"><h3>🔖 Your Sources (${S.us.length})</h3><p>Added by you — AI reviews these during scheduled updates</p></div>
      <div class="grid grid-3">${S.us.map((s,i)=>`<div class="card user-added news-item"><div class="ni-body">
        <h4><a href="${s.url}" target="_blank">${s.name||s.url}</a></h4>
        <div class="ni-meta"><span class="b" style="background:var(--bg);color:var(--text-muted)">Added ${s.addedDate||''}</span> <span class="b-ai">Pending AI review</span></div>
        <div class="ni-desc">${s.note||'Not yet reviewed'}</div>
        <button class="btn btn-d" onclick="S.us.splice(${i},1);save();fillNews()" style="margin-top:4px">✕ Remove</button>
      </div></div>`).join('')}</div>`:''
    ;
    el.innerHTML=userHtml+types.map(t=>{
      const items=S.news.filter(s=>s.type===t.k); if(!items.length)return '';
      return `<div class="sh" style="margin-top:10px"><h3>${t.l}</h3><p>${t.d}</p></div>
        <div class="grid grid-3">${items.map(s=>`<div class="card news-item" data-tip="${(s.tags||[]).join(', ')}"
          data-ai-source="${s.id}" data-ai-type="${s.type}" data-ai-free="${s.free}">
          <div class="ni-body">
            <h4><a href="${s.url}" target="_blank">${s.name}</a></h4>
            <div class="ni-meta"><span class="b" style="background:var(--bg);color:var(--text-muted)">${s.frequency}</span> ${s.free?'<span class="b b-free">Free</span>':'<span class="b b-paid">Paid</span>'}</div>
            <div class="ni-desc">${s.description}</div>
          </div></div>`).join('')}</div>`;
    }).join('');

  }else if(S.nst==='regs'){
    const countries=['all',...new Set(S.regs.map(r=>r.country))];
    const highImpact=S.regs.filter(r=>r.impact==='high').length;
    el.innerHTML=`
      <div class="info-grid">
        <div class="info-card"><div class="ic-value">${S.regs.length}</div><p>Total regulations tracked</p></div>
        <div class="info-card"><div class="ic-value" style="color:var(--danger)">${highImpact}</div><p>High impact policies</p></div>
        <div class="info-card"><div class="ic-value">${S.regs.filter(r=>r.status==='Enacted').length}</div><p>Currently enacted</p></div>
        <div class="info-card"><div class="ic-value">${S.regs.filter(r=>r.status==='In Progress').length}</div><p>In progress</p></div>
      </div>
      <div class="pills">${countries.map(c=>`<span class="pill${S.rf===c?' on':''}" onclick="S.rf='${c}';fillNews()">${c==='all'?'All Countries':c}</span>`).join('')}</div>
      ${(S.rf==='all'?S.regs:S.regs.filter(r=>r.country===S.rf)).map(r=>{
        const sc=r.status.toLowerCase().replace(/\s+/g,'-');
        return `<div class="card" data-tip="${r.country} · ${r.region} · ${r.impact} impact"
          data-ai-regulation="${r.id}" data-ai-status="${r.status}" data-ai-impact="${r.impact}">
          <div style="display:flex;justify-content:space-between;align-items:flex-start">
            <div>
              <h4 style="margin:0 0 3px;font-size:var(--font)"><a href="${r.url}" target="_blank" style="color:var(--text);text-decoration:none">${r.name}</a></h4>
              <div style="display:flex;gap:4px;flex-wrap:wrap;margin-bottom:4px">
                <span class="b-status ${sc}">${r.status}</span>
                <span class="b" style="background:${r.impact==='high'?'rgba(239,71,111,0.1)':r.impact==='medium'?'rgba(255,209,102,0.2)':'var(--bg)'};color:${r.impact==='high'?'var(--danger)':r.impact==='medium'?'#92400e':'var(--text-muted)'}">${r.impact} impact</span>
                <span class="b" style="background:var(--bg);color:var(--text-muted)">${r.country}</span>
              </div>
            </div>
          </div>
          <div style="font-size:var(--font-xs);color:var(--text-muted)">${r.summary}</div>
          ${r.effectiveDate?`<div style="font-size:10px;color:var(--text-muted);margin-top:3px">Effective: ${r.effectiveDate}</div>`:''}
        </div>`;
      }).join('')}`;

  }else if(S.nst==='landscape'){
    // AI landscape overview — what's happening RIGHT NOW
    const catData=S.cats.map(c=>{
      const tools=S.tools.filter(t=>t.category===c.id);
      const top=tools.sort((a,b)=>a.ranking.inCategory-b.ranking.inCategory)[0];
      const risingTools=tools.filter(t=>t.ranking.trend==='rising');
      return {c,tools,top,rising:risingTools};
    });
    el.innerHTML=`
      <div class="sh"><h3>AI Landscape — March 2026 Snapshot</h3>
        <p>A high-level view of where AI stands right now across every category we track. This is the "big picture" view.</p>
      </div>
      <div class="info-grid">
        <div class="info-card"><div class="ic-value">${S.tools.length}</div><p>Tools tracked across ${S.cats.length} categories</p></div>
        <div class="info-card"><div class="ic-value" style="color:var(--success)">${S.tools.filter(t=>t.pricingCAD.freeTier).length}</div><p>Offer free tiers — no risk to try</p></div>
        <div class="info-card"><div class="ic-value" style="color:var(--primary)">${S.tools.filter(t=>t.ranking.trend==='rising').length}</div><p>Rising fast — watch these closely</p></div>
        <div class="info-card"><div class="ic-value" style="color:var(--danger)">${S.tools.filter(t=>t.ranking.trend==='declining').length}</div><p>Declining — may be replaced soon</p></div>
      </div>
      ${catData.map(d=>`<div class="card" data-ai-landscape="${d.c.id}">
        <div style="display:flex;justify-content:space-between;align-items:flex-start">
          <div>
            <h4 style="margin:0;font-size:var(--font);color:${d.c.color}">${catIcon(d.c)} ${d.c.name}</h4>
            <p style="margin:2px 0;font-size:var(--font-xs);color:var(--text-muted)">${d.c.description}</p>
          </div>
          <span style="font-size:18px;font-weight:800;color:${d.c.color}">${d.tools.length}</span>
        </div>
        <div style="display:flex;gap:12px;margin-top:6px;font-size:var(--font-xs)">
          ${d.top?`<div><strong>Leader:</strong> <a href="${d.top.url}" target="_blank">${d.top.name}</a> (${d.top.developer})</div>`:''}
          ${d.rising.length?`<div><strong>Rising:</strong> ${d.rising.map(t=>`<a href="${t.url}" target="_blank">${t.name}</a>`).join(', ')}</div>`:''}
          <div><strong>Free options:</strong> ${d.tools.filter(t=>t.pricingCAD.freeTier).length}/${d.tools.length}</div>
        </div>
      </div>`).join('')}
      <div class="card" style="background:var(--primary-soft);border-color:var(--primary)">
        <h4 style="margin:0 0 4px;font-size:var(--font);color:var(--primary)">Key Trends — March 2026</h4>
        <ul style="margin:0;padding-left:16px;font-size:var(--font-xs);color:var(--text-muted);line-height:1.6">
          <li><strong>Video AI shakeup:</strong> Sora shut down. Runway, Kling, and Veo competing for dominance. Prices dropping fast.</li>
          <li><strong>Coding AI exploding:</strong> Claude Code hit $1B ARR in 6 months. Cursor passed 1M users. Non-devs are building real software.</li>
          <li><strong>Free tiers getting better:</strong> ${S.tools.filter(t=>t.pricingCAD.freeTier).length} of ${S.tools.length} tools offer usable free tiers — unprecedented access.</li>
          <li><strong>AI music is real:</strong> Suno v5 and Udio producing professional-grade tracks. ElevenLabs first to get YouTube monetization clearance.</li>
          <li><strong>Regulation accelerating:</strong> Canada's AIDA, EU AI Act enforcement starting, US executive orders. ${S.regs.filter(r=>r.status==='In Progress').length} policies in progress.</li>
          <li><strong>Local AI viable:</strong> Open-source models (DeepSeek, Qwen) competitive with cloud offerings. Privacy + zero cost.</li>
        </ul>
      </div>`;

  }else if(S.nst==='add'){
    el.innerHTML=`<div class="card">
      <h4 style="margin:0 0 6px;font-size:var(--font)">Add a Source</h4>
      <p style="font-size:var(--font-xs);color:var(--text-muted);margin:0 0 8px">Paste any URL — news site, YouTube channel, Reddit thread, tool page. Saved locally. <span class="b-ai">AI reviews for relevance</span> during scheduled updates and can auto-categorize it.</p>
      <div class="add-form"><input id="nu" type="url" placeholder="https://..."><input id="nn" placeholder="Name (optional)" style="max-width:160px"><button class="btn btn-p" onclick="addRes()">+ Add</button></div>
      <input id="no" placeholder="Why is this useful? (helps AI categorize)" style="width:100%;padding:6px 10px;border:1px solid var(--border);border-radius:var(--radius);font-size:var(--font-sm);background:var(--bg);color:var(--text);margin-top:4px;box-sizing:border-box">
      <div id="amsg" style="font-size:10px;margin-top:4px"></div></div>
      ${S.us.length?`<div class="sh" style="margin-top:8px"><h3>Your Sources (${S.us.length})</h3></div>${S.us.map((s,i)=>`<div class="card user-added" style="display:flex;justify-content:space-between;align-items:center"><div><a href="${s.url}" target="_blank" style="font-weight:600;font-size:var(--font-sm)">${s.name||s.url}</a> <span style="font-size:var(--font-xs);color:var(--text-muted)">${s.note||''}</span><div style="font-size:10px;color:var(--text-muted)">Added ${s.addedDate||'unknown'}</div></div><button class="btn btn-d" onclick="S.us.splice(${i},1);save();fillNews()">✕</button></div>`).join('')}`:''}`;
  }
}

function addRes(){
  const u=document.getElementById('nu')?.value?.trim(),n=document.getElementById('nn')?.value?.trim(),o=document.getElementById('no')?.value?.trim(),m=document.getElementById('amsg');
  if(!u||!u.startsWith('http')){if(m)m.textContent='Enter a valid URL';return;}
  if(S.us.some(s=>s.url===u)){if(m)m.textContent='Already added';return;}
  S.us.push({url:u,name:n||'',note:o||'',addedDate:new Date().toISOString().slice(0,10)});
  save(); if(m)m.innerHTML='<span style="color:var(--success)">✓ Added — will be reviewed by AI during next update</span>';
  document.getElementById('nu').value='';document.getElementById('nn').value='';document.getElementById('no').value='';
}

// ===== RANKINGS =====
function renderRankings(){
  const el=document.getElementById('tab-rankings');
  const sorted=[...S.tools].sort((a,b)=>a.ranking.overall-b.ranking.overall);
  const top15=sorted.slice(0,15);
  const bestFree=S.tools.filter(t=>t.pricingCAD.freeTier).sort((a,b)=>a.ranking.overall-b.ranking.overall).slice(0,10);
  const rising=S.tools.filter(t=>t.ranking.trend==='rising').sort((a,b)=>a.ranking.overall-b.ranking.overall);
  const bestVal=S.tools.filter(t=>t.pricingCAD.freeTier||(t.pricingCAD.paidPlans.length&&t.pricingCAD.paidPlans[0].priceCAD<=20)).sort((a,b)=>a.ranking.overall-b.ranking.overall).slice(0,10);
  const perCat=S.cats.map(c=>({c,t:S.tools.filter(t=>t.category===c.id).sort((a,b)=>a.ranking.inCategory-b.ranking.inCategory).slice(0,3)}));

  // Categorize free tiers
  const freeUnlimited=S.tools.filter(t=>{
    const lim=t.pricingCAD?.freeTierLimits;
    return t.pricingCAD.freeTier&&lim&&(lim.requestsPerDay==='unlimited'||lim.notes?.toLowerCase().includes('unlimited')||lim.notes?.toLowerCase().includes('open source'));
  });
  const freeLimited=S.tools.filter(t=>{
    const lim=t.pricingCAD?.freeTierLimits;
    return t.pricingCAD.freeTier&&lim&&!freeUnlimited.includes(t);
  });
  const freeNoLimits=S.tools.filter(t=>t.pricingCAD.freeTier&&!t.pricingCAD.freeTierLimits);
  const trialOnly=S.tools.filter(t=>{
    const lim=t.pricingCAD?.freeTierLimits;
    return t.pricingCAD.freeTier&&lim&&(lim.requestsPerDay===0||lim.notes?.toLowerCase().includes('trial')||lim.notes?.toLowerCase().includes('one-time'));
  });
  const paidOnly=S.tools.filter(t=>!t.pricingCAD.freeTier);

  el.innerHTML=`
    <div class="section-banner" data-ai-section="rankings" data-ai-description="AI tool rankings by category, value, momentum, and overall quality">
      <h2>Tool Rankings & Analysis</h2>
      <p>Who's winning, who's rising, who's dying — ranked by features, adoption, pricing, and growth trajectory</p>
      <div class="banner-stats">
        <span>#1 Overall: ${top15[0]?.name}</span>
        <span>${rising.length} tools rising</span>
        <span>Best free: ${bestFree[0]?.name}</span>
      </div>
    </div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:10px">
      <div class="chart-box"><h3>Most Popular (Top 15)</h3><div id="ch-popular"></div></div>
      <div class="chart-box"><h3>Tools per Category</h3><div id="ch1"></div></div>
      <div class="chart-box"><h3>Free vs Paid Breakdown</h3><div id="ch2"></div></div>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:10px">
      <div class="card"><div class="sh"><h3>🏆 Top 15 Overall</h3></div><ol class="rk">${top15.map((t,i)=>rkItem(t,i+1)).join('')}</ol></div>
      <div class="card"><div class="sh"><h3>🆓 Best Free Tiers</h3></div><ol class="rk">${bestFree.map((t,i)=>rkItem(t,i+1)).join('')}</ol></div>
      <div class="card"><div class="sh"><h3>💰 Best Value (&lt;$20 CAD/mo)</h3></div><ol class="rk">${bestVal.map((t,i)=>rkItem(t,i+1)).join('')}</ol></div>
      <div class="card"><div class="sh"><h3>📈 Rising Stars</h3></div><ol class="rk">${rising.map((t,i)=>rkItem(t,i+1)).join('')}</ol></div>
    </div>
    <div class="sh" style="margin-top:12px"><h2>Category Leaders</h2><p>Top 3 in each category</p></div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px">
      ${perCat.map(pc=>`<div class="card"><div class="sh"><h3><span style="color:${pc.c.color}">●</span> ${pc.c.name}</h3></div><ol class="rk">${pc.t.map((t,i)=>rkItem(t,i+1)).join('')}</ol></div>`).join('')}
    </div>`;

  if(typeof ApexCharts!=='undefined'){
    const dk=document.documentElement.getAttribute('data-theme')==='dark';
    const txtColor=dk?'#94a3b8':'#475569';

    // Most Popular bar chart (top 15 by ranking, inverted so #1 has longest bar)
    const maxRank=top15[top15.length-1]?.ranking.overall||100;
    new ApexCharts(document.getElementById('ch-popular'),{
      chart:{type:'bar',height:340,background:'transparent',toolbar:{show:false}},
      series:[{name:'Popularity Score',data:top15.map(t=>maxRank-t.ranking.overall+1)}],
      xaxis:{categories:top15.map(t=>t.name),labels:{style:{colors:txtColor,fontSize:'10px'}},axisBorder:{show:false}},
      yaxis:{show:false},
      plotOptions:{bar:{horizontal:true,borderRadius:3,barHeight:'70%',distributed:true}},
      colors:top15.map(t=>{const c=S.cats.find(x=>x.id===t.category);return c?c.color:'#64748b';}),
      legend:{show:false},
      dataLabels:{enabled:true,formatter:function(v,opts){return '#'+top15[opts.dataPointIndex]?.ranking.overall;},style:{fontSize:'10px',colors:['#fff']},offsetX:0},
      tooltip:{y:{formatter:function(v,opts){return '#'+top15[opts.dataPointIndex]?.ranking.overall+' overall';}}},
      grid:{show:false},
      theme:{mode:dk?'dark':'light'}
    }).render();

    // Tools per Category donut
    const cc=S.cats.map(c=>({n:c.name,v:S.tools.filter(t=>t.category===c.id).length,c:c.color}));
    new ApexCharts(document.getElementById('ch1'),{chart:{type:'donut',height:240,background:'transparent'},series:cc.map(c=>c.v),labels:cc.map(c=>c.n),colors:cc.map(c=>c.c),legend:{position:'bottom',fontSize:'10px',labels:{colors:dk?'#94a3b8':undefined}},plotOptions:{pie:{donut:{size:'55%'}}},theme:{mode:dk?'dark':'light'}}).render();

    // Free vs Paid breakdown donut (4 segments)
    new ApexCharts(document.getElementById('ch2'),{
      chart:{type:'donut',height:240,background:'transparent'},
      series:[freeUnlimited.length, freeLimited.length+freeNoLimits.length, trialOnly.length, paidOnly.length],
      labels:['Free Unlimited','Free (Limited Use)','Trial / Initial Credits','Paid Only'],
      colors:['#06d6a0','#4ecdc4','#ffd166','#ef476f'],
      legend:{position:'bottom',fontSize:'10px',labels:{colors:dk?'#94a3b8':undefined}},
      plotOptions:{pie:{donut:{size:'55%'}}},
      theme:{mode:dk?'dark':'light'}
    }).render();
  }
}

function rkItem(t,r){ const c=cat(t); return `<li data-tip="${t.description.substring(0,120)}..."
  data-ai-rank-item="${t.id}" data-ai-overall="${t.ranking.overall}">
  <span class="rk-n${r<=3?' gold':''}">${r}</span>
  <div class="rk-info"><span class="name"><a href="${t.url}" target="_blank" style="color:inherit;text-decoration:none">${t.name}</a></span> <span class="det">${c.name} · ${t.developer}${t.pricingCAD.freeTier?' · Free':''}</span></div>
  <span class="b b-trend ${t.ranking.trend}">${t.ranking.trend}</span></li>`; }

// ===== WORKFLOWS & PROJECTS =====
function renderFlows(){
  const el=document.getElementById('tab-workflows');
  const totalPhases=S.projects.reduce((a,p)=>a+p.phases.length,0);
  const wfs=Array.isArray(S.flows)?S.flows:(S.flows.workflows||[]);
  const verifiedCount=wfs.filter(w=>w.verified).length;
  const allSteps=wfs.flatMap(w=>(w.steps||[]));
  const toolsUsed=new Set(allSteps.map(s=>s.toolId)).size;
  el.innerHTML=`
    <div class="section-banner" data-ai-section="workflows-projects" data-ai-description="AI tool workflows and ambitious multi-AI projects">
      <h2>Workflows & Projects</h2>
      <p>From simple tool combinations to moonshot projects — no limits, no brick walls</p>
      <div class="banner-stats">
        <span>${wfs.length} workflows (${verifiedCount} verified)</span>
        <span>${S.projects.length} projects</span>
        <span>${totalPhases} phases planned</span>
        <span>${toolsUsed} tools used</span>
      </div>
    </div>
    <div class="stabs">
      <button class="stab${S.wst!=='projects'?' active':''}" onclick="S.wst='flows';renderFlows()">⚡ Workflows (${wfs.length})</button>
      <button class="stab${S.wst==='projects'?' active':''}" onclick="S.wst='projects';renderFlows()">🚀 Projects & Moonshots (${S.projects.length})</button>
    </div>
    <div id="wcontent"></div>`;
  if(S.wst==='projects') fillProjects(); else fillFlows();
}

function fillFlows(){
  const el=document.getElementById('wcontent'); if(!el)return;
  // Support both old array format and new object format
  const workflows=Array.isArray(S.flows)?S.flows:(S.flows.workflows||[]);
  el.innerHTML=`
    ${workflows.map(w=>{
      const steps=(w.steps||[]).map((s,i)=>{
        const t=S.tools.find(x=>x.id===s.toolId);
        const freeTag=s.free===false?'<span class="b" style="background:#ef476f;color:white;font-size:8px;margin-left:4px">PAID</span>':
          s.freeLimit?'<span class="b" style="background:#ffd166;color:#333;font-size:8px;margin-left:4px">LIMITED</span>':'';
        return `${i?'<span class="wf-arrow">→</span>':''}
        <div class="wf-step" data-tip="${s.action}"><span class="n">${s.order}</span><div><span class="t"><a href="${t?t.url:'#'}" target="_blank" style="color:inherit;text-decoration:none">${t?t.name:s.toolId}</a>${freeTag}</span><br><span class="a">${s.action}</span></div></div>`;
      }).join('');
      const verified=w.verified?'<span class="b" style="background:#06d6a0;color:white;font-size:8px">VERIFIED</span>':
        '<span class="b" style="background:var(--bg);color:var(--text-muted);font-size:8px">UNVERIFIED</span>';
      const costTag=w.costTier==='free'?'<span class="b" style="background:#06d6a0;color:white;font-size:8px">ALL FREE</span>':
        w.costTier==='mixed'?'<span class="b" style="background:#ffd166;color:#333;font-size:8px">FREE + PAID OPTIONS</span>':
        '<span class="b" style="background:#ef476f;color:white;font-size:8px">PAID</span>';
      const connectors=(w.connectors||[]).map(c=>
        `<span class="b" style="background:var(--bg);color:var(--text-muted);font-size:8px" data-tip="${c.note||''}">${c.type}: ${c.name}</span>`
      ).join(' ');
      const gaps=(w.gaps||[]).map(g=>`<div style="font-size:var(--font-xs);color:var(--warning);margin-top:2px">⚠ ${g}</div>`).join('');
      const insight=w.keyInsight?`<div style="font-size:var(--font-xs);color:var(--primary);margin-top:6px;padding:4px 6px;background:var(--primary-soft);border-radius:4px">💡 ${w.keyInsight}</div>`:'';
      const freeAlt=w.freeAlternative?`<div style="font-size:var(--font-xs);color:var(--success);margin-top:2px">🆓 Free alternative: ${w.freeAlternative}</div>`:'';
      return `<div class="card" data-ai-workflow="${w.id}">
        <h3 style="margin:0 0 3px;font-size:var(--font);font-weight:700">${w.name}</h3>
        <div style="font-size:var(--font-xs);color:var(--text-muted);margin-bottom:8px">${w.description}</div>
        <div style="margin-bottom:6px;display:flex;flex-wrap:wrap;gap:4px">
          ${verified} ${costTag}
          <span class="b" style="background:var(--bg);color:var(--text-muted)">${w.difficulty||'intermediate'}</span>
          <span class="b" style="background:var(--bg);color:var(--text-muted)">${w.category||''}</span>
        </div>
        <div class="wf-steps">${steps}</div>
        ${connectors?'<div style="margin-top:6px;display:flex;flex-wrap:wrap;gap:3px">'+connectors+'</div>':''}
        ${insight}${freeAlt}${gaps}
        ${w.verifiedSource?'<div style="font-size:9px;color:var(--text-muted);margin-top:4px">Source: '+w.verifiedSource+'</div>':''}
      </div>`;
    }).join('')}
    <div class="card" style="background:var(--primary-soft);border-color:var(--primary)">
      <h4 style="margin:0 0 4px;font-size:var(--font);color:var(--primary)">💡 Build Your Own Workflow</h4>
      <p style="margin:0;font-size:var(--font-xs);color:var(--text-muted)">These are verified starting points from real users. The Phase 2 orchestrator can generate custom workflows for any task — just describe what you need.</p>
    </div>`;
}

function fillProjects(){
  const el=document.getElementById('wcontent'); if(!el)return;
  const ambColors={high:'var(--primary)',moonshot:'var(--purple)'};
  const statusColors={'in-progress':'var(--success)',concept:'var(--primary)',planned:'var(--warning)'};
  el.innerHTML=`
    <div class="card" style="background:rgba(114,9,183,0.06);border-color:var(--purple);margin-bottom:12px">
      <h4 style="margin:0 0 4px;font-size:var(--font);color:var(--purple)">🧠 The Philosophy</h4>
      <p style="margin:0;font-size:var(--font-xs);color:var(--text-muted);line-height:1.6"><strong>Nothing is a brick wall.</strong> These projects assume unlimited time and resources in their design — then we find the cheapest, fastest path to actually build them. When a roadblock appears, we throw every AI tool at it. When one AI can't do something, another can. When no AI can do it yet, we document exactly what's missing and watch for when it becomes possible.</p>
      <p style="margin:4px 0 0;font-size:var(--font-xs);color:var(--text-muted)"><strong>The question isn't "can this be done?" — it's "which combination of tools gets us closest, and what's the gap?"</strong></p>
    </div>
    ${S.projects.map(p=>`<div class="card" data-ai-project="${p.id}" style="border-left:4px solid ${ambColors[p.ambition]||'var(--primary)'}">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px">
        <div>
          <h3 style="margin:0;font-size:15px;font-weight:800">${p.name}</h3>
          <div style="display:flex;gap:4px;margin-top:4px">
            <span class="b" style="background:${ambColors[p.ambition]||'var(--primary)'};color:white">${p.ambition}</span>
            <span class="b" style="background:${statusColors[p.status]||'var(--bg)'};color:white">${p.status}</span>
          </div>
        </div>
      </div>
      <p style="font-size:var(--font-xs);color:var(--text-muted);margin:6px 0">${p.description}</p>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:8px 0;font-size:var(--font-xs)">
        <div style="padding:6px;background:var(--bg);border-radius:4px"><strong>Now:</strong> ${p.currentState}</div>
        <div style="padding:6px;background:rgba(6,214,160,0.08);border-radius:4px"><strong>Goal:</strong> ${p.targetState}</div>
      </div>
      <div style="margin-top:8px">
        ${p.phases.map(ph=>`<div style="padding:8px;margin-bottom:6px;background:var(--bg);border-radius:6px;border-left:3px solid ${statusColors[ph.status]||'var(--border)'}">
          <div style="display:flex;justify-content:space-between;align-items:center">
            <h4 style="margin:0;font-size:var(--font-sm);font-weight:700">Phase ${ph.phase}: ${ph.name}</h4>
            <span class="b" style="background:${statusColors[ph.status]||'var(--bg)'};color:white;font-size:9px">${ph.status}</span>
          </div>
          <p style="margin:3px 0;font-size:var(--font-xs);color:var(--text-muted)">${ph.description}</p>
          <details style="margin-top:4px"><summary style="font-size:var(--font-xs);cursor:pointer;color:var(--primary);font-weight:600">Tasks · Tools · Cost · Blockers</summary>
            <div style="margin-top:6px;font-size:var(--font-xs)">
              <div style="margin-bottom:4px"><strong>Tasks:</strong><ul style="margin:2px 0;padding-left:16px;color:var(--text-muted)">${ph.tasks.map(t=>'<li>'+t+'</li>').join('')}</ul></div>
              <div style="margin-bottom:4px"><strong>AI Tools:</strong> ${ph.aiTools.map(t=>'<span class="b-ai" style="margin-right:2px">'+t+'</span>').join('')}</div>
              <div style="margin-bottom:4px"><strong>Cost:</strong> <span style="color:var(--success)">${ph.estimatedCost}</span></div>
              ${ph.blockers.length?`<div style="margin-bottom:4px"><strong style="color:var(--danger)">Blockers:</strong> ${ph.blockers.join(' · ')}</div>`:''}
              ${ph.workarounds.length?`<div><strong style="color:var(--success)">Workarounds:</strong><ul style="margin:2px 0;padding-left:16px;color:var(--text-muted)">${ph.workarounds.map(w=>'<li>'+w+'</li>').join('')}</ul></div>`:''}
            </div>
          </details>
        </div>`).join('')}
      </div>
      <div style="display:flex;justify-content:space-between;font-size:10px;color:var(--text-muted);margin-top:4px;padding-top:6px;border-top:1px solid var(--border)">
        <span>⚠️ Biggest risk: ${p.biggestRisk}</span>
        <span>✅ Mitigation: ${p.mitigation}</span>
      </div>
    </div>`).join('')}`;
}

// ===== STRATEGIES =====
function renderStrategies(){
  const el=document.getElementById('tab-strategies');
  if(!el)return;
  const strats=S.strats;
  const cats=[...new Set(strats.map(s=>s.category))];
  const totalStrats=strats.reduce((a,s)=>a+(s.strategies?s.strategies.length:0),0);

  const diffColors={beginner:'var(--success)',intermediate:'var(--warning)',advanced:'var(--danger)'};
  const costColors={free:'var(--success)',low:'var(--primary)',medium:'var(--warning)',high:'var(--danger)'};

  el.innerHTML=`
    <div class="section-banner" data-ai-section="strategies" data-ai-description="Workarounds and strategies for overcoming AI tool limitations">
      <h2>Overcoming Limitations</h2>
      <p>Every obstacle has a workaround — here's the playbook</p>
      <div class="banner-stats">
        <span>${strats.length} challenges documented</span>
        <span>${totalStrats} strategies compiled</span>
        <span>${cats.length} categories covered</span>
      </div>
    </div>
    <div class="info-grid">
      <div class="info-card"><div class="ic-value">${strats.length}</div><p>Total strategies</p></div>
      <div class="info-card"><div class="ic-value">${cats.length}</div><p>Categories covered</p></div>
    </div>
    ${cats.map(catName=>{
      const items=strats.filter(s=>s.category===catName);
      return `<div class="sh" style="margin-top:12px"><h3>${catName}</h3></div>
        ${items.map(s=>`<div class="card" data-ai-strategy="${s.id}" style="border-left:4px solid var(--primary)">
          <h3 style="margin:0 0 4px;font-size:15px;font-weight:800">${s.title}</h3>
          <p style="font-size:var(--font-xs);color:var(--text-muted);margin:0 0 8px">${s.description}</p>
          ${s.currentState?`<div style="padding:6px;background:var(--bg);border-radius:4px;margin-bottom:6px;font-size:var(--font-xs)"><strong>Current State:</strong> ${s.currentState}</div>`:''}
          <div style="margin:8px 0">
            ${(s.strategies||[]).map(st=>`<div style="padding:8px;margin-bottom:6px;background:var(--bg);border-radius:6px">
              <div style="display:flex;justify-content:space-between;align-items:center">
                <h4 style="margin:0;font-size:var(--font-sm);font-weight:700">${st.name}</h4>
                <div style="display:flex;gap:4px">
                  ${st.difficulty?`<span class="b" style="background:${diffColors[st.difficulty]||'var(--bg)'};color:white;font-size:9px">${st.difficulty}</span>`:''}
                  ${st.cost?`<span class="b" style="background:${costColors[st.cost]||'var(--bg)'};color:white;font-size:9px">${st.cost}</span>`:''}
                </div>
              </div>
              <p style="margin:3px 0 0;font-size:var(--font-xs);color:var(--text-muted)">${st.how}</p>
            </div>`).join('')}
          </div>
          ${s.futureState?`<div style="padding:6px;background:rgba(6,214,160,0.08);border-radius:4px;font-size:var(--font-xs)"><strong>Future State:</strong> ${s.futureState}</div>`:''}
        </div>`).join('')}`;
    }).join('')}`;
}

// ===== COMMAND CENTER =====
function renderCommandCenter(){
  const el=document.getElementById('tab-command-center'); if(!el)return;
  const briefs=S.briefs.sort((a,b)=>b.date.localeCompare(a.date));
  const latest=briefs[0]||null;
  const pipes=S.auto.pipelines||[];
  const goals=S.auto.automationGoals||[];
  const activePipes=pipes.filter(p=>p.status==='active').length;
  const plannedPipes=pipes.filter(p=>p.status==='planned').length;

  el.innerHTML=`
    <div class="section-banner" data-ai-section="command-center">
      <h2>\u{1F9E0} Command Center</h2>
      <p>Autonomous AI research system — gathers intelligence, synthesizes findings, proposes actions</p>
      <div class="banner-stats">
        <span>${briefs.length} briefings</span>
        <span>${activePipes} active pipelines</span>
        <span>${plannedPipes} planned pipelines</span>
        <span>${S.tools.length} tools tracked</span>
      </div>
    </div>

    <div class="stabs">
      <button class="stab${S.cst==='briefs'||!S.cst?' active':''}" onclick="S.cst='briefs';renderCommandCenter()">📋 Briefings (${briefs.length})</button>
      <button class="stab${S.cst==='pipelines'?' active':''}" onclick="S.cst='pipelines';renderCommandCenter()">⚡ Automation (${pipes.length})</button>
      <button class="stab${S.cst==='goals'?' active':''}" onclick="S.cst='goals';renderCommandCenter()">🎯 Autonomy Progress</button>
    </div>
    <div id="cc-content"></div>`;

  const cc=document.getElementById('cc-content');
  if(!S.cst||S.cst==='briefs') {
    cc.innerHTML=briefs.length?briefs.map(b=>`
      <div class="card" style="margin-bottom:12px" data-ai-briefing="${b.id}">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">
          <div>
            <span class="b" style="background:${b.type==='alert'?'var(--danger)':b.type==='weekly'?'var(--primary)':'var(--success)'};color:white">${b.type.toUpperCase()}</span>
            <strong style="margin-left:8px">${b.title}</strong>
          </div>
          <span style="color:var(--text-muted);font-size:var(--font-xs)">${b.date}</span>
        </div>
        <p style="color:var(--text-muted);margin-bottom:8px">${b.summary}</p>
        ${(b.sections||[]).map(s=>`
          <div style="border-left:3px solid ${s.impact==='high'?'var(--danger)':s.impact==='medium'?'var(--warning)':'var(--success)'};padding-left:10px;margin:8px 0">
            <strong>${s.heading}</strong> <span class="b" style="font-size:10px">${s.impact} impact</span>
            <p style="color:var(--text-muted);font-size:var(--font-sm);margin:4px 0">${s.content}</p>
            ${s.actionItems?.length?'<div style="margin-top:4px">'+s.actionItems.map(a=>'<div style="font-size:var(--font-xs);color:var(--primary)">\u2192 '+a+'</div>').join('')+'</div>':''}
          </div>`).join('')}
        ${(b.newDiscoveries||[]).length?`<div style="margin-top:8px;padding-top:8px;border-top:1px solid var(--border)"><strong style="font-size:var(--font-sm)">\u{1F50D} New Discoveries</strong>${b.newDiscoveries.map(d=>`<div style="font-size:var(--font-sm);margin:4px 0"><a href="${d.url}" target="_blank">${d.name}</a> — ${d.why}</div>`).join('')}</div>`:''}
      </div>`).join(''):'<div class="card"><p style="color:var(--text-muted)">No briefings yet. Set up the daily research scheduled task to start receiving intelligence reports.</p></div>';
  } else if(S.cst==='pipelines') {
    cc.innerHTML=`
      <div class="info-grid" style="margin-bottom:12px">
        <div class="info-card"><div class="ic-value">${activePipes}</div><p>Active</p></div>
        <div class="info-card"><div class="ic-value">${plannedPipes}</div><p>Planned</p></div>
        <div class="info-card"><div class="ic-value">${pipes.filter(p=>p.status==='concept').length}</div><p>Concept</p></div>
      </div>
      ${pipes.map(p=>`
        <div class="card" style="margin-bottom:8px">
          <div style="display:flex;justify-content:space-between;align-items:flex-start">
            <div>
              <span class="b" style="background:${p.status==='active'?'var(--success)':p.status==='planned'?'var(--warning)':'var(--text-muted)'};color:white">${p.status}</span>
              <span class="b" style="margin-left:4px">${p.engine}</span>
              <strong style="margin-left:8px">${p.name}</strong>
            </div>
            <span style="color:var(--text-muted);font-size:var(--font-xs)">${p.schedule}</span>
          </div>
          <p style="color:var(--text-muted);font-size:var(--font-sm);margin:6px 0">${p.description}</p>
          <div style="font-size:var(--font-xs);color:var(--text-muted)">
            ${p.steps.map(s=>`<span style="margin-right:8px">${s.order}. ${s.action}</span>`).join(' \u2192 ')}
          </div>
          <div style="font-size:var(--font-xs);margin-top:4px;color:var(--text-muted)">Outputs: ${p.outputs.join(', ')}</div>
        </div>`).join('')}`;
  } else if(S.cst==='goals') {
    cc.innerHTML=goals.map(g=>`
      <div class="card" style="margin-bottom:8px">
        <div style="display:flex;justify-content:space-between;align-items:center">
          <strong>Level ${g.level}: ${g.name}</strong>
          <span class="b" style="background:var(--primary);color:white">${g.currentProgress}</span>
        </div>
        <p style="color:var(--text-muted);font-size:var(--font-sm);margin:6px 0">${g.description}</p>
        <div style="background:var(--bg);border-radius:4px;height:6px;margin:6px 0"><div style="background:var(--primary);height:100%;border-radius:4px;width:${g.currentProgress}"></div></div>
        ${g.blockers?.length?'<div style="font-size:var(--font-xs);color:var(--danger)">Blockers: '+g.blockers.join(', ')+'</div>':''}
        ${g.nextSteps?.length?'<div style="font-size:var(--font-xs);color:var(--success);margin-top:4px">Next: '+g.nextSteps.join(' \u2192 ')+'</div>':''}
      </div>`).join('');
  }
}

// ===== ABOUT =====
function renderAbout(){
  const el=document.getElementById('tab-about');
  const dc=Object.values(S.ts).filter(v=>v==='deleted').length;
  const tried=Object.values(S.ts).filter(v=>v==='tried').length;
  el.innerHTML=`<div class="about">
    <div class="section-banner">
      <h2>About This System</h2>
      <p>An AI assistant for AI guidance, testing & development</p>
    </div>

    <div class="info-grid" style="margin-top:12px">
      <div class="info-card"><h4>Version</h4><div class="ic-value">${S.meta?.version||'?'}</div><p>Last updated ${S.meta?.lastUpdated||'?'}</p></div>
      <div class="info-card"><h4>Data</h4><div class="ic-value">${S.tools.length} tools</div><p>${S.cats.length} categories · ${S.news.length} sources · ${S.regs.length} regs</p></div>
      <div class="info-card"><h4>Your Progress</h4><div class="ic-value">${tried}/${S.tests.length}</div><p>Tests completed · ${dc} dismissed</p></div>
      <div class="info-card"><h4>Exchange Rate</h4><div class="ic-value">$${S.meta?.cadExchangeRate}</div><p>USD → CAD · All prices in CAD</p></div>
    </div>

    <h3>The Vision</h3>
    <p>This isn't just a dashboard — it's the foundation for an <strong>AI intelligence system</strong> that helps you keep up with AI progress, test new tools hands-on, and understand what's possible. It amasses information, proposes actions, and grows smarter over time.</p>
    <p><strong>Nothing is a brick wall.</strong> If a tool needs testing, AI can open a browser. If data is stale, AI can research it. If something new launches, AI can detect it and propose a test. The scope expands as we discover what's possible.</p>

    <h3>What Needs AI vs What's Standalone</h3>
    <table>
      <tr><td><strong>Standalone</strong> — works right now, no AI needed</td><td></td></tr>
      <tr><td style="padding-left:16px">Dashboard, search, filters, dark mode, density</td><td><span class="b-standalone">Standalone</span></td></tr>
      <tr><td style="padding-left:16px">Try/save/dismiss tests, drag-and-drop reorder</td><td><span class="b-standalone">Standalone</span></td></tr>
      <tr><td style="padding-left:16px">Rankings, charts, workflow references</td><td><span class="b-standalone">Standalone</span></td></tr>
      <tr><td style="padding-left:16px">Add custom sources, export data</td><td><span class="b-standalone">Standalone</span></td></tr>
      <tr><td style="margin-top:8px"><strong>AI-Powered</strong> — requires an AI assistant</td><td></td></tr>
      <tr><td style="padding-left:16px">Research new tools, verify pricing, detect shutdowns</td><td><span class="b-ai">AI + web</span></td></tr>
      <tr><td style="padding-left:16px">Scan news sources for breaking developments</td><td><span class="b-ai">AI + web</span></td></tr>
      <tr><td style="padding-left:16px">Generate new tests when tools launch</td><td><span class="b-ai">AI + analysis</span></td></tr>
      <tr><td style="padding-left:16px">Review user-submitted URLs for relevance</td><td><span class="b-ai">AI + web fetch</span></td></tr>
      <tr><td style="padding-left:16px">Open browser windows for hands-on testing</td><td><span class="b-ai">AI + browser</span></td></tr>
      <tr><td style="padding-left:16px">Run automated comparisons and benchmarks</td><td><span class="b-ai">AI + automation</span></td></tr>
      <tr><td style="padding-left:16px">Predict which tools will dominate</td><td><span class="b-ai">AI + reasoning</span></td></tr>
      <tr><td style="padding-left:16px">Create custom code to overcome obstacles</td><td><span class="b-ai">AI + coding</span></td></tr>
    </table>

    <h3>How It Updates</h3>
    <ul>
      <li><strong>Claude Scheduled Tasks</strong> — Daily AI research (configurable): new tools, pricing changes, shutdowns, news, regulation updates, stale data detection, broken links</li>
      <li><strong>GitHub Actions</strong> — Weekly JSON validation + metadata refresh</li>
      <li><strong>Manual</strong> — Edit JSON in <code>data/</code> folder, or add sources via AI News tab</li>
      <li><strong>On-demand</strong> — Ask AI to research a specific topic, tool, or question</li>
    </ul>

    <h3>Architecture</h3>
    <p>Modular JSON data files — each section loads independently. No frameworks, no build tools, no server required. Opens in any browser. Every piece is replaceable: swap the CSS framework, change the AI assistant, host anywhere. The JSON data is the real asset — the UI is just one way to view it.</p>
    <p><code>data-ai-*</code> attributes throughout the HTML make this machine-readable. Any AI can parse the DOM or the JSON files directly to understand the full state of the system.</p>

    <h3>AI Tool Selection</h3>
    <p>Currently uses Claude. Design goal: allow selecting which AI handles each task (ChatGPT for research, Gemini for Google integration, local models for privacy). The system is tool-agnostic by design — the JSON data works with any AI.</p>

    <h3>Settings</h3>
    <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:6px">
      ${dc?`<button class="btn btn-o" onclick="Object.keys(S.ts).forEach(k=>{if(S.ts[k]==='deleted')delete S.ts[k]});save();renderAbout()">↩ Restore ${dc} dismissed</button>`:''}
      <button class="btn btn-o" onclick="if(confirm('Reset all local data? (tests, sources, preferences)')){S.ts={};S.to=[];S.us=[];localStorage.removeItem('ai-dash');location.reload()}">Reset all data</button>
    </div>
  </div>`;
}

function updFoot(){ const f=document.getElementById('dashboard-footer'); if(f&&S.meta) f.textContent=`AI Intelligence Hub v${S.meta.version} · ${S.meta.lastUpdated} · CAD ($1 USD ≈ $${S.meta.cadExchangeRate} CAD) · Point-in-time snapshot`; }
