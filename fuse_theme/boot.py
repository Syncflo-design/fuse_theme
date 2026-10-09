"""What the desk needs from the theme before the first page paints.

Two things, both read by fuse_theme.bundle.js:

  * `home` — the workspace this user calls home, when it is not Fuse Home. An industry app
    ships its own desk page (Construction, say); a login pointed at it by its default
    workspace lands there, and the house button takes it back there.
  * `tiles` — how an app wants the shortcuts on its desk page drawn: an icon and a line of
    description per shortcut, so they read as Fuse tiles rather than bare links. Apps declare
    them through a `fuse_desk_tiles` hook, the same way they contribute Fuse Home tiles.

This runs on every desk load. Nothing in it may raise: a boot hook that fails stops the
whole desk from loading, which is a far worse outcome than plain shortcuts.
"""

import frappe

from fuse_theme.install import LANDING


def extend(bootinfo):
	try:
		bootinfo.fuse_desk = {"home": _home_workspace(), "tiles": _desk_tiles()}
	except Exception:
		frappe.log_error(title="Fuse Theme: desk boot data", message=frappe.get_traceback())
		bootinfo.fuse_desk = {"home": None, "tiles": {}}


def _home_workspace():
	"""The user's own desk page, or None when their home is Fuse Home.

	The landing workspace counts as Fuse Home: it exists only to send people there, because
	a default workspace cannot point at a Page.
	"""
	if frappe.session.user == "Guest":
		return None
	name = frappe.db.get_value("User", frappe.session.user, "default_workspace")
	if not name or name == LANDING:
		return None
	return name


def _desk_tiles():
	"""{workspace name: {shortcut label: {"svg": ..., "blurb": ...}}} from every app.

	A contributor that raises is skipped, as with Fuse Home tiles: its desk shows plain
	shortcuts, and every other app's desk is unaffected.
	"""
	tiles = {}
	for method in frappe.get_hooks("fuse_desk_tiles") or []:
		try:
			for workspace, shortcuts in (frappe.get_attr(method)() or {}).items():
				tiles.setdefault(workspace, {}).update(shortcuts)
		except Exception:
			continue
	return tiles
