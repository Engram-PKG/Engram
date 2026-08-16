/* ============================================================
   APP.JS — shared behaviour across all Digital Twin pages
   ============================================================ */

const DT = (() => {

  /* ---------- tiny state helpers (localStorage-backed mock) ---------- */
  const store = {
    get(key, fallback){
      try{
        const v = localStorage.getItem('dt_' + key);
        return v ? JSON.parse(v) : fallback;
      }catch(e){ return fallback; }
    },
    set(key, value){
      try{ localStorage.setItem('dt_' + key, JSON.stringify(value)); }catch(e){}
    }
  };

  /* ---------- auth forms (login / signup) ---------- */
  function initAuthForm(formId, redirectTo){
    const form = document.getElementById(formId);
    if(!form) return;
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const alertBox = form.querySelector('.form-alert');
      const btn = form.querySelector('button[type="submit"]');
      const requiredFields = [...form.querySelectorAll('[required]')];
      const allFilled = requiredFields.every(f => f.value.trim().length > 0);

      if(!allFilled){
        if(alertBox){
          alertBox.textContent = 'Fill in every field before continuing.';
          alertBox.classList.remove('success');
          alertBox.classList.add('show','error');
        }
        return;
      }

      if(alertBox){
        alertBox.textContent = 'Success — redirecting to your twin…';
        alertBox.classList.remove('error');
        alertBox.classList.add('show','success');
      }
      if(btn){ btn.textContent = 'Please wait…'; btn.disabled = true; }
      store.set('authed', true);
      setTimeout(() => { window.location.href = redirectTo; }, 700);
    });
  }

  /* ---------- connectors page ---------- */
  function initConnectors(){
    const grid = document.querySelector('[data-connector-grid]');
    if(!grid) return;

    grid.addEventListener('click', (e) => {
      const btn = e.target.closest('.connector-toggle-btn');
      if(!btn) return;
      const card = btn.closest('.connector-card');
      const statusEl = card.querySelector('.connector-status');
      const nowConnected = !btn.classList.contains('is-connected');

      if(nowConnected){
        openConnectorModal(card.dataset.name || 'this source', () => {
          btn.classList.add('is-connected');
          btn.textContent = 'Disconnect';
          statusEl.classList.add('connected');
          statusEl.innerHTML = '<span class="dot"></span> Connected';
          updateConnectorCount();
        });
      } else {
        btn.classList.remove('is-connected');
        btn.textContent = 'Connect';
        statusEl.classList.remove('connected');
        statusEl.innerHTML = '<span class="dot"></span> Not connected';
        updateConnectorCount();
      }
    });

    // category filter chips
    const chips = document.querySelectorAll('.connector-category-tabs .filter-chip');
    chips.forEach(chip => {
      chip.addEventListener('click', () => {
        chips.forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        const cat = chip.dataset.filter;
        grid.querySelectorAll('.connector-card').forEach(card => {
          card.style.display = (cat === 'all' || card.dataset.category === cat) ? '' : 'none';
        });
      });
    });

    updateConnectorCount();
  }

  function updateConnectorCount(){
    const countEl = document.querySelector('[data-connected-count]');
    if(!countEl) return;
    const connected = document.querySelectorAll('.connector-toggle-btn.is-connected').length;
    countEl.textContent = connected;
  }

  function openConnectorModal(name, onConfirm){
    const overlay = document.getElementById('permissionModal');
    if(!overlay){ onConfirm(); return; }
    overlay.querySelector('[data-modal-source-name]').textContent = name;
    overlay.classList.add('open');
    const confirmBtn = overlay.querySelector('[data-modal-confirm]');
    const cancelBtns = overlay.querySelectorAll('[data-modal-cancel]');

    const cleanup = () => {
      overlay.classList.remove('open');
      confirmBtn.removeEventListener('click', onConfirmClick);
    };
    const onConfirmClick = () => { cleanup(); onConfirm(); };

    confirmBtn.addEventListener('click', onConfirmClick, { once: true });
    cancelBtns.forEach(b => b.addEventListener('click', cleanup, { once: true }));
  }

  /* ---------- building / onboarding sequence ---------- */
  function initBuildingSequence(nextPage){
    const ring = document.querySelector('[data-progress-bar]');
    const pctLabel = document.querySelector('[data-progress-pct]');
    const logItems = [...document.querySelectorAll('.build-log .log-item')];
    if(!ring) return;

    const circumference = 2 * Math.PI * 118; // matches r=118 in svg
    ring.style.strokeDasharray = `${circumference}`;
    ring.style.strokeDashoffset = `${circumference}`;

    let step = 0;
    const totalSteps = logItems.length;

    function advance(){
      if(step > 0) logItems[step-1].classList.replace('active','done');
      if(step >= totalSteps){
        setTimeout(() => { window.location.href = nextPage; }, 600);
        return;
      }
      logItems[step].classList.add('active');
      const pct = Math.round(((step+1) / totalSteps) * 100);
      const offset = circumference - (pct/100) * circumference;
      ring.style.strokeDashoffset = `${offset}`;
      if(pctLabel) pctLabel.textContent = `${pct}%`;
      step++;
      setTimeout(advance, 1100);
    }
    setTimeout(advance, 500);
  }

  /* ---------- chat ---------- */
  const twinReplies = [
    "Looking back at your calendar, you tend to protect Tuesday mornings for deep work — want me to guard that time this week too?",
    "Based on the messages you've sent this month, you've mentioned feeling stretched thin around deadlines three times. Want to talk through what's driving that?",
    "I pulled this from your notes app: you wrote about wanting to read more fiction in Q1. You've logged two books so far — should I suggest a third?",
    "Comparing this to how you usually respond to similar requests, I'd lean toward saying yes but setting a clear boundary on scope.",
    "I noticed a pattern across your last five journal entries — mornings are when you're most decisive. Want me to schedule around that?",
    "That's consistent with what you told your team last quarter. I can draft a reply that keeps the same tone if that helps."
  ];

  function initChat(){
    const scroll = document.querySelector('[data-chat-scroll]');
    const form = document.querySelector('[data-composer-form]');
    const textarea = document.querySelector('[data-composer-input]');
    if(!scroll || !form || !textarea) return;

    textarea.addEventListener('input', () => {
      textarea.style.height = 'auto';
      textarea.style.height = Math.min(textarea.scrollHeight, 140) + 'px';
    });

    textarea.addEventListener('keydown', (e) => {
      if(e.key === 'Enter' && !e.shiftKey){
        e.preventDefault();
        form.requestSubmit();
      }
    });

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const text = textarea.value.trim();
      if(!text) return;
      appendMessage('user', text);
      textarea.value = '';
      textarea.style.height = 'auto';
      showTyping();
      const delay = 900 + Math.random()*900;
      setTimeout(() => {
        removeTyping();
        const reply = twinReplies[Math.floor(Math.random()*twinReplies.length)];
        appendMessage('twin', reply, true);
      }, delay);
    });

    function appendMessage(who, text, withSource){
      const msg = document.createElement('div');
      msg.className = `msg from-${who}`;
      const time = new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});
      msg.innerHTML = `
        <div class="avatar">${who === 'twin' ? twinBadgeHTML() : '🙂'}</div>
        <div>
          <div class="bubble">${escapeHTML(text)}</div>
          ${withSource ? `<div class="chat-source-chip">⟡ drawn from 3 memories</div>` : ''}
          <div class="msg-meta">${time}</div>
        </div>`;
      scroll.appendChild(msg);
      scroll.scrollTop = scroll.scrollHeight;
    }

    function showTyping(){
      const t = document.createElement('div');
      t.className = 'msg from-twin';
      t.id = 'typingMsg';
      t.innerHTML = `
        <div class="avatar">${twinBadgeHTML()}</div>
        <div class="bubble"><div class="typing-indicator"><span></span><span></span><span></span></div></div>`;
      scroll.appendChild(t);
      scroll.scrollTop = scroll.scrollHeight;
    }
    function removeTyping(){
      const t = document.getElementById('typingMsg');
      if(t) t.remove();
    }
    function twinBadgeHTML(){
      return `<div class="thread-badge" style="width:32px;height:32px;"><div class="core" style="width:10px;height:10px;"></div></div>`;
    }
    function escapeHTML(str){
      const div = document.createElement('div');
      div.textContent = str;
      return div.innerHTML;
    }
  }

  /* ---------- generic filter chips (timeline / connectors category use this too) ---------- */
  function initFilterChips(containerSelector, itemSelector, attr){
    const container = document.querySelector(containerSelector);
    if(!container) return;
    const chips = container.querySelectorAll('.filter-chip');
    chips.forEach(chip => {
      chip.addEventListener('click', () => {
        chips.forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        const val = chip.dataset.filter;
        document.querySelectorAll(itemSelector).forEach(item => {
          item.style.display = (val === 'all' || item.dataset[attr] === val) ? '' : 'none';
        });
      });
    });
  }

  /* ---------- live search filter (search.html) ---------- */
  function initSearchPage(){
    const input = document.querySelector('[data-live-search]');
    const results = document.querySelectorAll('[data-result-item]');
    const emptyState = document.querySelector('[data-search-empty]');
    if(!input) return;
    input.addEventListener('input', () => {
      const q = input.value.trim().toLowerCase();
      let visible = 0;
      results.forEach(item => {
        const text = item.textContent.toLowerCase();
        const match = q === '' || text.includes(q);
        item.style.display = match ? '' : 'none';
        if(match) visible++;
      });
      if(emptyState) emptyState.style.display = visible === 0 ? 'block' : 'none';
    });
  }

  /* ---------- settings toggles ---------- */
  function initSettings(){
    const nav = document.querySelectorAll('.settings-nav a');
    const sections = document.querySelectorAll('[data-settings-section]');
    nav.forEach(link => {
      link.addEventListener('click', (e) => {
        if(link.dataset.section){
          e.preventDefault();
          nav.forEach(l => l.classList.remove('active'));
          link.classList.add('active');
          sections.forEach(s => {
            s.style.display = s.dataset.settingsSection === link.dataset.section ? 'block' : 'none';
          });
        }
      });
    });

    const dangerBtn = document.querySelector('[data-delete-twin]');
    if(dangerBtn){
      dangerBtn.addEventListener('click', () => {
        if(confirm('This permanently deletes your digital twin and all learned memories. Continue?')){
          alert('Twin deletion scheduled. You can cancel within 14 days from Settings → Account.');
        }
      });
    }
  }

  /* ---------- reflection actions ---------- */
  function initReflections(){
    document.querySelectorAll('[data-reflection-dismiss]').forEach(btn => {
      btn.addEventListener('click', () => {
        const card = btn.closest('.reflection-card');
        card.style.transition = 'opacity .3s, transform .3s';
        card.style.opacity = '0';
        card.style.transform = 'translateY(-8px)';
        setTimeout(() => card.remove(), 300);
      });
    });
  }

  /* ---------- mobile rail toggle (if hamburger present) ---------- */
  function initMobileNav(){
    const toggle = document.querySelector('[data-nav-toggle]');
    const rail = document.querySelector('.rail, .site-header');
    if(!toggle || !rail) return;
    toggle.addEventListener('click', () => rail.classList.toggle('open'));
  }

  return {
    store,
    initAuthForm,
    initConnectors,
    initBuildingSequence,
    initChat,
    initFilterChips,
    initSearchPage,
    initSettings,
    initReflections,
    initMobileNav
  };
})();
