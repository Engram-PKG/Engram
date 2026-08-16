/* ============================================================
   ANIMATION.JS — the twin-thread motif, ambient particles,
   and the force-directed knowledge graph canvas.
   ============================================================ */

const DTAnim = (() => {

  /* ---------- build the twin-thread svg into any container ---------- */
  function mountTwinThread(selector){
    const el = document.querySelector(selector);
    if(!el) return;
    el.innerHTML = `
      <svg viewBox="0 0 220 220">
        <defs>
          <linearGradient id="threadGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#FF8B5E"/>
            <stop offset="100%" stop-color="#6EE7C0"/>
          </linearGradient>
        </defs>
        <path class="thread-line" d="M 54 110 Q 110 60 166 110" />
        <circle class="orb-you" cx="54" cy="110" r="20"/>
        <circle class="orb-twin" cx="166" cy="110" r="20"/>
      </svg>`;
  }

  /* ---------- ambient drifting particle field (hero / building bg) ---------- */
  function mountAmbientField(selector, count = 18){
    const el = document.querySelector(selector);
    if(!el) return;
    const frag = document.createDocumentFragment();
    for(let i=0; i<count; i++){
      const dot = document.createElement('span');
      dot.style.left = Math.random()*100 + '%';
      dot.style.top = Math.random()*100 + '%';
      dot.style.animationDuration = (4 + Math.random()*5) + 's';
      dot.style.animationDelay = (Math.random()*4) + 's';
      dot.style.opacity = (0.2 + Math.random()*0.5).toFixed(2);
      frag.appendChild(dot);
    }
    el.appendChild(frag);
  }

  /* ---------- knowledge graph canvas ----------
     A tiny force-ish layout: nodes gently orbit + connections pulse.
     data: [{id, label, group}], links: [{source, target}]
  ------------------------------------------------- */
  function mountKnowledgeGraph(canvasSelector, data, links){
    const canvas = document.querySelector(canvasSelector);
    if(!canvas) return;
    const ctx = canvas.getContext('2d');
    let w, h;

    function resize(){
      const rect = canvas.parentElement.getBoundingClientRect();
      w = canvas.width = rect.width * devicePixelRatio;
      h = canvas.height = rect.height * devicePixelRatio;
      canvas.style.width = rect.width + 'px';
      canvas.style.height = rect.height + 'px';
      ctx.setTransform(devicePixelRatio,0,0,devicePixelRatio,0,0);
    }
    window.addEventListener('resize', resize);
    resize();

    const colors = { core: '#6EE7C0', person: '#FF8B5E', topic: '#8892A0', event: '#6EE7C0' };

    // seed positions in a circle, with slight per-node orbit radius/speed
    const cw = () => canvas.getBoundingClientRect().width;
    const ch = () => canvas.getBoundingClientRect().height;

    data.forEach((n, i) => {
      const angle = (i / data.length) * Math.PI * 2;
      n._baseAngle = angle;
      n._orbitR = n.group === 'core' ? 0 : 90 + Math.random()*140;
      n._speed = 0.0003 + Math.random()*0.0004;
      n._r = n.group === 'core' ? 22 : 10 + Math.random()*6;
    });

    let t = 0;
    function frame(){
      t += 1;
      const width = cw(), height = ch();
      ctx.clearRect(0,0,width,height);
      const cx = width/2, cy = height/2;

      data.forEach(n => {
        const angle = n._baseAngle + t * n._speed;
        n.x = cx + Math.cos(angle) * n._orbitR;
        n.y = cy + Math.sin(angle) * n._orbitR * 0.72;
      });

      // links
      links.forEach(l => {
        const a = data.find(n => n.id === l.source);
        const b = data.find(n => n.id === l.target);
        if(!a || !b) return;
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.strokeStyle = 'rgba(110,231,192,0.18)';
        ctx.lineWidth = 1;
        ctx.stroke();
      });

      // nodes
      data.forEach(n => {
        ctx.beginPath();
        ctx.arc(n.x, n.y, n._r, 0, Math.PI*2);
        ctx.fillStyle = colors[n.group] || '#8892A0';
        ctx.globalAlpha = n.group === 'core' ? 1 : 0.85;
        ctx.shadowColor = colors[n.group] || '#8892A0';
        ctx.shadowBlur = n.group === 'core' ? 30 : 14;
        ctx.fill();
        ctx.globalAlpha = 1;
        ctx.shadowBlur = 0;

        ctx.font = n.group === 'core' ? '600 13px Inter, sans-serif' : '500 11px Inter, sans-serif';
        ctx.fillStyle = n.group === 'core' ? '#0B0E14' : '#E8ECF1';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        if(n.group === 'core'){
          ctx.fillText(n.label, n.x, n.y);
        } else {
          ctx.fillStyle = '#E8ECF1';
          ctx.fillText(n.label, n.x, n.y + n._r + 13);
        }
      });

      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);

    // click detection -> dispatch custom event with node id
    canvas.addEventListener('click', (e) => {
      const rect = canvas.getBoundingClientRect();
      const mx = e.clientX - rect.left, my = e.clientY - rect.top;
      const hit = data.find(n => Math.hypot(n.x-mx, n.y-my) <= n._r + 4);
      if(hit){
        canvas.dispatchEvent(new CustomEvent('nodeclick', { detail: hit, bubbles: true }));
      }
    });
  }

  return { mountTwinThread, mountAmbientField, mountKnowledgeGraph };
})();
