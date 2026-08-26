# Graph Report - C:\ClaudeCode\fuse_theme  (2026-08-26)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 79 nodes · 101 edges · 14 communities (11 shown, 3 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 1 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `997a0be4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- api.py
- FuseHome
- after_install
- manifest.json
- fuse_theme.bundle.js
- FuseTraining
- fuse_theme

## God Nodes (most connected - your core abstractions)
1. `FuseHome` - 12 edges
2. `after_install()` - 9 edges
3. `FuseTraining` - 7 edges
4. `get_training_documents()` - 6 edges
5. `get_home()` - 5 edges
6. `setup()` - 4 edges
7. `_all_tiles()` - 3 edges
8. `_active_modules()` - 3 edges
9. `_shipped_guides()` - 3 edges
10. `_branding()` - 3 edges

## Surprising Connections (you probably didn't know these)
- `setup()` --calls--> `after_install()`  [EXTRACTED]
  fuse_theme/api.py → fuse_theme/install.py

## Import Cycles
- None detected.

## Communities (14 total, 3 thin omitted)

### Community 0 - "api.py"
Cohesion: 0.17
Nodes (16): _active_modules(), _all_tiles(), _file_size(), get_home(), get_training_documents(), whitelist, Data for the Fuse home page. One whitelisted call returns everything the page…, The tiles above, plus whatever another Fuse app contributes. A separately sold… (+8 more)

### Community 2 - "after_install"
Cohesion: 0.21
Nodes (12): after_install(), _branding(), _build(), whitelist, Site configuration the theme owns. Wired to after_install AND after_migrate,…, Put Fuse's own logo on the login screen, the navbar and the browser tab. Set…, The folder guides are uploaded into, created if it is not there yet., Create or refresh one workspace. Rebuilt from this definition every time rather… (+4 more)

### Community 3 - "manifest.json"
Cohesion: 0.18
Nodes (10): background_color, description, display, icons, name, orientation, scope, short_name (+2 more)

### Community 4 - "fuse_theme.bundle.js"
Cohesion: 0.36
Nodes (8): at_desk_root(), build_button(), DESK_ROOTS, go_home_if_at_root(), head_link(), insert_button(), install_pwa_head(), start()

## Knowledge Gaps
- **12 isolated node(s):** `DESK_ROOTS`, `name`, `short_name`, `description`, `start_url` (+7 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `after_install()` connect `after_install` to `api.py`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Why does `setup()` connect `api.py` to `after_install`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **What connects `DESK_ROOTS`, `name`, `short_name` to the rest of the system?**
  _12 weakly-connected nodes found - possible documentation gaps or missing edges._