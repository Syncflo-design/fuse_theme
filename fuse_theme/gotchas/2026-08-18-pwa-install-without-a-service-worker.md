# Fuse installs as a phone app with no service worker — and deliberately so

**Date:** 2026-08-18
**Applies to:** `fuse_theme` (manifest + head links), any Frappe desk you want installable

## Symptom

Chrome shows no "Install app" option on a Frappe desk, and the shop-floor screens
open in a browser tab with the address bar eating the top of a phone screen.

## Cause

Frappe has **no hook for adding anything to the desk's `<head>`**. `app_include_js`
and `app_include_css` exist; there is no `app_include_head`. So a `<link
rel="manifest">` cannot be declared the way it would be on an ordinary site, and
without it Chrome has nothing to install.

## Fix

Inject the head links from the desk JS bundle (`app_include_js` runs on every desk
page, which is exactly the scope the manifest covers):

- `fuse_theme/public/manifest.json` — served at `/assets/fuse_theme/manifest.json`.
  Everything in `public/` is symlinked into `sites/assets/<app>/`, so a plain JSON
  file needs no build step and no route.
- `fuse_theme.bundle.js` appends `install_pwa_head()`, which adds the manifest link,
  an `apple-touch-icon`, `apple-mobile-web-app-capable` and `theme-color`. Each one
  checks for itself first, so route changes cannot duplicate them.

`scope` is `/app/` and `start_url` is `/app/fuse-floor`. Scope is validated against
the **start URL**, not against where the manifest file itself is served from — a
manifest under `/assets/` scoping `/app/` is valid.

## Two things that are easy to get wrong

**No service worker, on purpose.** Chrome dropped the service-worker requirement
for installability; a manifest, HTTPS and an icon of at least 144px are enough. A
worker caching desk assets would also fight the Frappe Cloud deploy cycle — a stale
bundle held in a phone's cache is
`CoWork_Helper/gotchas/2026-05-06-frappe-cloud-cdn-stale-assets.md` with no way to
clear it from your side. Installed means *own icon, own window*, not *works
offline*: every floor screen posts to Intacct and none of them can work without a
connection.

**Icons must be square and big enough.** `fuse-icon.png` is 100×100 — under
Chrome's 144px floor, so it would have failed silently. `fuse-app-192.png`,
`fuse-app-512.png` and a maskable 512 are generated from the sphere in
`fuse-logo.png`, on white, with the maskable one at 60% coverage so an Android
launcher can crop the corners to any shape without cutting into the artwork. The
wordmark is left out — unreadable at 192px, same reason the apps-screen entry uses
the sphere alone.

## See also

- `CoWork_Helper/gotchas/2026-05-06-frappe-cloud-cdn-stale-assets.md`
- `Fuse_Manufacturing/fuse_manufacturing/docs/03-decisions.md` — 2026-08-18, the
  shop-floor screens the install exists to reach
