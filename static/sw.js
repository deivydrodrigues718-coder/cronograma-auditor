const CACHE_NAME = 'rfb-cronograma-v1';
const URLS = [
    '/',
    '/disciplinas',
    '/revisoes',
    '/estatisticas',
    '/static/manifest.json'
];

self.addEventListener('install', e => {
    e.waitUntil(
        caches.open(CACHE_NAME).then(cache => cache.addAll(URLS))
    );
});

self.addEventListener('fetch', e => {
    e.respondWith(
        caches.match(e.request).then(response => response || fetch(e.request))
    );
});
