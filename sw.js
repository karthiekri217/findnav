// sw.js
self.addEventListener('install', (event) => {
    console.log('[ServiceWorker] Install');
    event.waitUntil(
        caches.open('v1').then((cache) => {
            return cache.addAll([
                './',
                './index.html',
                './styles.css',
                './app.js',
                './manifest.json',
                './icon-192.png',
                './icon-512.png'
            ]);
        })
    );
});

self.addEventListener('fetch', (event) => {
    console.log('[ServiceWorker] Fetch', event.request.url);
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request).catch(() => {
                return new Response("Network error occurred!", {
                    status: 408,
                    statusText: "Network Error"
                });
            });
        })
    );
});
