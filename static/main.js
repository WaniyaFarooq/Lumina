/* ════════════════════════════════════════
   LUMINA INTERACTIONS — JS ENGINE (FIXED)
════════════════════════════════════════ */
document.querySelector(".result-content").innerHTML =
  response.replace(/\n/g, "<br>");
document.addEventListener('DOMContentLoaded', () => {

  /* ───────────── CUSTOM CURSOR ───────────── */
  const dot = document.querySelector('.cursor-dot');
  const ring = document.querySelector('.cursor-ring');

  if (dot && ring) {
    document.addEventListener('mousemove', e => {
      dot.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`;
      ring.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`;
    });

    document.querySelectorAll('a, button, .btn, .card, .option-btn').forEach(el => {
      el.addEventListener('mouseenter', () => {
        dot.classList.add('is-hover');
        ring.classList.add('is-hover');
      });
      el.addEventListener('mouseleave', () => {
        dot.classList.remove('is-hover');
        ring.classList.remove('is-hover');
      });
    });
  }

  /* ───────────── CURSOR TRAIL ───────────── */
  document.addEventListener('mousemove', e => {
    const trail = document.createElement('div');
    trail.className = 'trail-dot';
    trail.style.left = e.clientX + 'px';
    trail.style.top = e.clientY + 'px';
    document.body.appendChild(trail);

    setTimeout(() => trail.remove(), 400);
  });

  /* ───────────── MAGNETIC BUTTONS ───────────── */
  document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('mousemove', e => {
      const rect = btn.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;

      btn.style.transform = `translate(${x * 0.2}px, ${y * 0.3}px)`;
    });

    btn.addEventListener('mouseleave', () => {
      btn.style.transform = 'translate(0,0)';
    });
  });

  /* ───────────── CARD 3D TILT ───────────── */
  document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;

      card.style.transform = `
        rotateX(${y * -10}deg)
        rotateY(${x * 12}deg)
        scale(1.02)
      `;

      card.style.setProperty('--mx', `${e.clientX - rect.left}px`);
      card.style.setProperty('--my', `${e.clientY - rect.top}px`);
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = 'rotateX(0) rotateY(0) scale(1)';
    });
  });

  /* ───────────── SCROLL REVEAL ───────────── */
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
      }
    });
  }, { threshold: 0.15 });

  document.querySelectorAll('.reveal-item').forEach(el => {
    observer.observe(el);
  });

  /* ───────────── BUTTON RIPPLE EFFECT ───────────── */
  document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('click', e => {
      const ripple = document.createElement('span');
      ripple.classList.add('ripple');

      const rect = btn.getBoundingClientRect();
      ripple.style.left = (e.clientX - rect.left) + 'px';
      ripple.style.top = (e.clientY - rect.top) + 'px';

      btn.appendChild(ripple);

      setTimeout(() => ripple.remove(), 600);
    });
  });

  /* ───────────── NAV INDICATOR ───────────── */
  const nav = document.querySelector('nav');

  if (nav) {
    const indicator = document.createElement('div');
    indicator.classList.add('nav-indicator');
    nav.appendChild(indicator);

    const links = document.querySelectorAll('.nav-link');

    links.forEach(link => {
      link.addEventListener('mouseenter', () => {
        const rect = link.getBoundingClientRect();
        const navRect = nav.getBoundingClientRect();

        indicator.style.width = rect.width + 'px';
        indicator.style.left = (rect.left - navRect.left) + 'px';
      });
    });
  }

 

});