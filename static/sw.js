const CACHE_NAME = 'palin-os-v84';
const STATIC_ASSETS = [
  '/',
  '/css/style.css',
  '/js/app.js',
  '/manifest.json'
];

// Install - cache core static assets only
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting();
});

// Activate - clean all old caches immediately
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Fetch - DO NOT cache API requests (Security & Privacy guarantee)
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  
  // 🚫 API 요청, 관리자 페이지, 인증 관련 요청은 절대로 캐시하지 않고 항상 네트워크 직접 통신
  if (event.request.method !== 'GET' || url.pathname.startsWith('/api/') || url.pathname.includes('admin')) {
    return;
  }
  
  event.respondWith(
    fetch(event.request)
      .then(response => {
        if (response && response.status === 200 && response.type === 'basic') {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        }
        return response;
      })
      .catch(() => caches.match(event.request))
  );
});
