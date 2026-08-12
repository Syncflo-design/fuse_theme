# Landing users on a custom Page in Frappe v16

**Seen:** 2026-08-11, leader-rubber-co (v16.30 / ERPNext 16.31).

Getting users to land on the Fuse Home page took far longer than it should have. What is
actually true on this stack:

## The routes

- **`/app` redirects to `/desk`.** The desk is `/desk` in v16. Advice to "use /app instead"
  is wrong here and wasted a round trip.
- Users always arrive at `/desk`, and the desk's home button goes there too.

## What the `/desk` root actually renders

A grid of **workspaces, labelled by `title`, not `label`**. That one detail caused a long
detour: querying `Workspace.label` returned "Invoicing", "Home", "Build" — none of which
matched the on-screen "Accounting", "Organization" — so the grid looked like it was neither
workspaces nor modules. It was workspaces the whole time.

**When identifying a screen, fetch `title` as well as `name`/`label`.**

## What does NOT work

- `home_page` / `role_home_page` hooks — website only, no effect on the desk.
- `User.default_workspace` — takes a **Workspace**, not a Page. Lands one click away.
- `User.default_app` — its description says "Redirect to the selected app after login", and
  `add_to_apps_screen` does register the app (confirmed via `frappe.apps.get_apps`), but it
  did not change where `/desk` lands.

## What does work

The theme claims the desk root in its own JS (`fuse_theme.bundle.js`):

```js
if (path === '/desk' || path === '/app') frappe.set_route('fuse-home');
```

Run on load AND on `frappe.router.on('change')` — the home button routes in-app without a
page load, so a boot-time check alone misses it. Plus an `F` button injected into the
navbar as a permanent way back.

## Verifying a front-end deploy without logging in

Assets are public, so the site can be checked directly:

- `/assets/assets.json` — the build manifest; confirms the bundle was built and gives its
  hashed filename
- `/assets/<app>/dist/js/<bundle>.<hash>.js` — fetch it and grep for a string from the
  change

That proves the code is live in two requests, rather than asking the user to keep
refreshing.
