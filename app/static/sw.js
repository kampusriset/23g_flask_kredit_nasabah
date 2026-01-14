// Service Worker for SIPINA PWA
const CACHE_NAME = 'sipina-cache-v1';

self.addEventListener('install', (event) => {
  console.log('Service Worker installed');
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  console.log('Service Worker activated');
});

self.addEventListener('fetch', (event) => {
  // Basic pass-through fetch for now
  event.respondWith(fetch(event.request));
});
