const CACHE_NAME = 'kp-v1';
const OFFLINE_URL = './index.html';

// ===== INSTALL =====
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.add(OFFLINE_URL))
  );
  self.skipWaiting();
});

// ===== ACTIVATE =====
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// ===== FETCH — cache-first =====
self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    caches.match(e.request).then(cached =>
      cached || fetch(e.request).catch(() => caches.match(OFFLINE_URL))
    )
  );
});

// ===== TIMER BACKGROUND (BroadcastChannel) =====
const timerChannel = new BroadcastChannel('kp-timer');
let activeTimer = null;

timerChannel.addEventListener('message', (e) => {
  const { type } = e.data;

  if (type === 'START_TIMER') {
    if (activeTimer) clearInterval(activeTimer.interval);
    let remaining = e.data.duration_ms;
    const { taskId, taskName } = e.data;

    const interval = setInterval(() => {
      remaining -= 1000;
      timerChannel.postMessage({ type: 'TICK', remaining_ms: remaining, taskId });

      if (remaining <= 0) {
        clearInterval(interval);
        activeTimer = null;
        timerChannel.postMessage({ type: 'TIMER_DONE', taskId });

        // Notificación push cuando expira
        self.registration.showNotification('⚔ Killer Pendiente', {
          body: `"${taskName}" — El tiempo ha llegado. ¿Lo mataste?`,
          icon: './icon.svg',
          badge: './icon.svg',
          vibrate: [200, 100, 200, 100, 400],
          tag: 'kp-timer-done',
          renotify: true,
          requireInteraction: true,
          data: { taskId }
        });
      }
    }, 1000);

    activeTimer = { interval, taskId };
  }

  if (type === 'STOP_TIMER') {
    if (activeTimer) {
      clearInterval(activeTimer.interval);
      activeTimer = null;
    }
  }

  if (type === 'PAUSE_TIMER') {
    if (activeTimer) {
      clearInterval(activeTimer.interval);
      // Guarda remaining para reanudar
      activeTimer.paused_at = e.data.remaining_ms;
    }
  }
});

// ===== NOTIFICACIÓN CLICK =====
self.addEventListener('notificationclick', (e) => {
  e.notification.close();
  e.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then(cs => {
      const found = cs.find(c => c.url.includes('index.html'));
      if (found) return found.focus();
      return clients.openWindow('./index.html');
    })
  );
});
