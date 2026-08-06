# fuse_theme

Fuse Manufacturing look and feel for Frappe / ERPNext v16. Sage Intacct inspired,
green base `#007E45`.

Companion to `fuse_manufacturing` (the Intacct integration app). The two are separate
apps on purpose: a colour change here must never force an integration release, and not
every client wants the Intacct look.

## What it does

Ships one stylesheet, `fuse_theme.bundle.css`, loaded via `app_include_css`. It sets
Frappe's own CSS variables to the Fuse palette and restyles existing desk components —
navbar, sidebar, workspace tiles, list/report grids, buttons, forms, status pills,
dialogs.

Tokens are lifted verbatim from the donor app's own theme
(`SBMS/assets/css/fuse-theme.css`) so the two products read as the same family.

## The rule

**Style, do not restructure.**

Colour, typography, density, nav treatment and button styling survive framework
upgrades. Rearranging form layouts or replacing framework components to mimic a
legacy screen does not — it fights Frappe on every release.

If a screen needs a different *shape*, that belongs in `fuse_manufacturing` as a real
page or DocType, not in here as CSS that fakes it.

## Install

```bash
bench get-app fuse_theme <repo-url>
bench --site <site> install-app fuse_theme
bench build --app fuse_theme
bench --site <site> clear-cache
```

After deploying to Frappe Cloud, trigger a fresh **Deploy** rather than **Update** —
Update runs migrations but skips `bench build`, so the CSS stays stale.

## Status

v0.1.0 — written against the donor theme, **not yet rendered on a live site**.
Component selectors (navbar, sidebar, widget, list-row, datatable) need verifying
against the actual v16 desk markup once the bench is up; the CSS-variable block will
hold regardless, the component rules may need selector corrections.
