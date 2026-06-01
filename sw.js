/* Service Worker - gudaoqihuo.com */
const CACHE_NAME = 'gudaoqihuo-v1';
const CACHE_URLS = [
  '/',
  '/index.html',
  '/en/index.html'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(CACHE_URLS))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});
