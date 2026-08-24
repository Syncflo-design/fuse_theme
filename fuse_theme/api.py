"""Data for the Fuse home page.

One whitelisted call returns everything the page paints. Tiles are declared here
rather than in a DocType: there is one product, one tile set, and a record-driven
tile library is only worth its weight once admins need to add tiles themselves.

Each tile's `route` is a frappe.set_route argument array. `options` is applied as
frappe.route_options first, which Frappe treats as list filters on a List route and as
field defaults on a new document — one mechanism for both.

Every tile that moves stock lands on a Stock Entry of a specific type. That is not
cosmetic: only the purposes in fuse_manufacturing.postings.POSTED_PURPOSES post to
Intacct, so a tile that drops the user on an untyped form invites them to pick one that
moves stock locally and tells Intacct nothing.
"""

import frappe

# Stock Entry types that post. Kept as literals rather than imported from the integration
# app: the theme must install and run without it, and a missing tile is a better failure
# than a home page that will not load.
TRANSFER = "Material Transfer"
WIP_ISSUE = "Material Transfer for Manufacture"

TILES = [
	{
		# On the second row with BOMs and Projects rather than in the run of actions: this
		# states what is needed, it does not move anything. The moving is Receiving's job,
		# further down.
		#
		# On a site integrated with Intacct the purchase order itself is mirrored FROM
		# Intacct and is read-only here, so this is a request someone acts on there.
		# Standalone, it is the whole requisition step.
		#
		# The blurb names all of what the record does. A Material Request can ask to buy, to
		# move stock between warehouses, or to make something — and it is raised by stores or
		# a planner as often as by anyone on the floor, so it does not claim an audience.
		"key": "material_request",
		"label": "Material Request",
		"blurb": "Request material to buy, move or make",
		"icon": "📝",
		"route": ["List", "Material Request"],
		"group": "reference",
		"roles": ["Stock Controller", "Stock User", "Stock Manager", "Purchase User",
		          "Purchase Manager", "Manufacturing User", "Manufacturing Manager"],
	},
	{
		# Goods in. Lives in fuse_manufacturing — it moves stock — so it is guarded by
		# `requires_page` and simply does not appear on a site without that app.
		#
		# Emoji here, not SVG, only because its four neighbours are emoji and one odd
		# tile out looks like a fault. When the tile grid moves to an icon set, this
		# moves with it.
		"key": "receiving",
		"label": "Receiving",
		"blurb": "Book a delivery in against a purchase order",
		"icon": "📥",
		"route": ["fuse-receiving"],
		"requires_page": "fuse-receiving",
		"roles": ["Stock Controller", "Stock User", "Stock Manager"],
	},
	{
		# Ahead of Works Orders on purpose: the tiles read left to right as the process
		# does — what a thing is made of, what that means we should make, then making it.
		"key": "boms",
		"label": "BOMs",
		"blurb": "What each product is made of",
		"icon": "📋",
		"route": ["List", "BOM"],
		# Set apart on its own row. A BOM is not something you DO — it is what the doing is
		# based on, the same way a project is the thing work is booked against. Mixing them
		# into the run of actions made the row read as nine equal verbs.
		"group": "reference",
		"roles": ["Stock Controller", "Manufacturing User", "Manufacturing Manager"],
	},
	{
		"key": "production_plan",
		"label": "Production Plan",
		"blurb": "Work out what to make and what to buy",
		"icon": "🗓",
		"route": ["List", "Production Plan"],
		# Manufacturing User is the only role ERPNext grants Production Plan out of the
		# box. The others are here for sites that have widened it; the permission check
		# below still decides.
		"roles": ["Manufacturing User", "Manufacturing Manager", "Stock Controller"],
	},
	{
		# Goods out, and the mirror of Receiving above: same screen pointed the other way,
		# living in fuse_manufacturing because it moves stock, so it simply does not appear
		# on a site without that app.
		"key": "picking",
		"label": "Picking",
		"blurb": "Send goods out against a customer order",
		"icon": "🚚",
		"route": ["fuse-picking"],
		"requires_page": "fuse-picking",
		"roles": ["Stock Controller", "Stock User", "Stock Manager"],
	},
	{
		"key": "works_orders",
		"label": "Works Orders",
		"blurb": "Current manufacturing and production orders",
		"icon": "🔧",
		"route": ["List", "Work Order"],
		"roles": ["Stock Controller", "Manufacturing User", "Manufacturing Manager"],
	},
	{
		"key": "wip_issue",
		"label": "Issue to WIP",
		"blurb": "Move components into a work-in-progress warehouse",
		"icon": "🏭",
		"route": ["new", "Stock Entry"],
		"options": {"stock_entry_type": WIP_ISSUE},
		"roles": ["Stock Controller", "Manufacturing User", "Manufacturing Manager"],
	},
	{
		# The donor had this split into Quick (one item) and Bulk (several). In ERPNext
		# they are the same document with a different number of rows, so two tiles led to
		# the same form. One tile, and a scanner-shaped single-item screen can be added
		# later if the shop floor wants one.
		"key": "item_transfer",
		"label": "Item Transfer",
		"blurb": "Move stock between warehouses",
		"icon": "⇄",
		"route": ["new", "Stock Entry"],
		"options": {"stock_entry_type": TRANSFER},
		"roles": ["Stock Controller", "Stock User", "Stock Manager"],
	},
	{
		# ERPNext's own Stock workspace — the full module, for someone who needs more than
		# the shortcuts above. The route is the workspace SLUG for the same reason as
		# stock_control below: ["Workspaces", "Stock"] builds a URL the desk answers with
		# empty skeletons. That is what this line said for weeks while doing the opposite.
		#
		# OFF by default (see fuse_manufacturing.modules). Two tiles onto a stock workspace
		# read as two doors into the same room, and Stock Control is the curated one. A
		# client whose own admin wants the full module switches it on.
		"key": "stock",
		"label": "Stock",
		"blurb": "General stock management",
		"icon": "🗃",
		"route": ["stock"],
		"roles": ["Stock Controller", "Stock User", "Stock Manager"],
	},
	{
		"key": "stock_control",
		"label": "Stock Control",
		"blurb": "Transfers, production and stock reports",
		"icon": "📦",
		# The workspace SLUG, not ["Workspaces", "Fuse Stock Control"]. That older form
		# builds /desk/Workspaces/Fuse%20Stock%20Control, which renders as empty skeletons
		# and throws in frappe.views.Workspace.show_page — the fault that looked like a
		# permissions problem for days. The desk's own sidebar uses the slug, and the slug
		# works.
		"route": ["fuse-stock-control"],
		"roles": ["Stock Controller", "Stock User", "Stock Manager"],
	},
]


def _all_tiles():
	"""The tiles above, plus whatever another Fuse app contributes.

	A separately sold part of Fuse ships as its own app and cannot edit this list. It
	declares a `fuse_tiles` hook pointing at a callable that returns tiles in the same
	shape; its tile is then filtered by the same rules and switched off by the same Active
	Modules table as the built-in ones.

	A contributor that raises is skipped. A missing tile is a poor outcome; a home page
	that will not load because an optional app is half-installed is a worse one.
	"""
	tiles = list(TILES)
	for method in frappe.get_hooks("fuse_tiles") or []:
		try:
			tiles.extend(frappe.get_attr(method)() or [])
		except Exception:
			continue
	return tiles


def _active_modules():
	"""What the client has switched on, or everything if we cannot tell.

	The switches live in fuse_core, which the theme must run without — so a site with no
	Fuse apps at all shows every tile. Failing open is right here: the alternative is a home
	page that quietly loses its tiles because an unrelated app is absent, which looks like
	the theme is broken.
	"""
	try:
		from fuse_core import modules
	except ImportError:
		return {}

	try:
		return modules.active_modules()
	except Exception:
		# Installed but not yet migrated — the settings table may not exist on the first
		# load after a deploy. Same reasoning: show everything rather than nothing.
		return {}


@frappe.whitelist()
def get_home():
	"""Tiles this user may actually use, plus what the header needs.

	Filtered by role AND by read permission on the target doctype — a tile the user
	cannot open is worse than no tile, because it looks like the system is broken
	rather than like they lack access.
	"""
	roles = set(frappe.get_roles())
	active = _active_modules()

	tiles = []
	for tile in _all_tiles():
		# Switched off by the client under Active Modules in Intacct Settings. Checked
		# first because it is a decision someone made deliberately, where a role or a
		# permission miss is usually an oversight.
		if not active.get(tile["key"], True):
			continue
		# A tile that names no roles is for everyone — a contributed tile is not obliged
		# to name any.
		if tile.get("roles") and not roles.intersection(tile["roles"]):
			continue
		if tile["route"][0] in ("List", "new") and not frappe.has_permission(tile["route"][1], "read"):
			continue
		# A tile that creates something needs create rights, not just read. Otherwise it
		# opens a form the user cannot save, which reads as a broken system rather than as
		# a permission they do not have.
		if tile["route"][0] == "new" and not frappe.has_permission(tile["route"][1], "create"):
			continue
		# A tile belonging to another app is hidden when that app is not installed. A
		# dead route reads as a broken system; a missing tile reads as a feature this
		# site does not have, which is the truth.
		if tile.get("requires_page") and not frappe.db.exists("Page", tile["requires_page"]):
			continue
		tiles.append({k: v for k, v in tile.items() if k not in ("roles", "requires_page")})

	return {
		"tiles": tiles,
		# The shop-floor screens are NOT a tile. They live in fuse_manufacturing and
		# their real entry point is the installed app, whose start_url opens them
		# directly — an operator on a phone never sees this page at all. The footer
		# link exists so the concept can be shown from a desk without giving it
		# equal billing with the modules people use all day.
		#
		# None when fuse_manufacturing is not installed: the theme must run without
		# it, and a dead link reads as a broken system.
		"floor": {"route": "fuse-floor", "label": "Shop floor screens"}
		if frappe.db.exists("Page", "fuse-floor") and active.get("shop_floor", True)
		else None,
		# Help, on every instance. The guides ship with the apps, so this is never a link to
		# an empty page — which is what it would have been on any site nobody uploaded to.
		"training": {"route": "fuse-training", "label": "Guides"}
		if frappe.db.exists("Page", "fuse-training")
		else None,
		"user": frappe.db.get_value("User", frappe.session.user, "full_name") or frappe.session.user,
		"company": frappe.defaults.get_user_default("Company") or "",
	}


# Where the guides live. One folder, so the Training page and the upload button can never
# disagree about what counts as a guide.
TRAINING_FOLDER = "Home/Fuse Training"


def _shipped_guides():
	"""Guides that travel with the installed apps.

	Each Fuse app declares its own through the `fuse_guides` hook, so Manufacturing ships the
	stock guides and Projects will ship the project ones — the theme, which owns the page
	they appear on, needs to know about neither.

	A contributor that raises is skipped. A missing guide is a poor outcome; a Training page
	that will not load because one app is half-installed is a worse one.
	"""
	guides = []
	for method in frappe.get_hooks("fuse_guides") or []:
		try:
			guides.extend(frappe.get_attr(method)() or [])
		except Exception:
			continue
	return guides


@frappe.whitelist()
def get_training_documents():
	"""The guides: what the installed apps ship, plus whatever this site has uploaded.

	Shipped guides mean a new instance is never installed without help. Uploads are read
	from the folder rather than a list in code, so replacing one on a single site is an
	upload and nothing else — no code change, no deploy.

	An upload with the same title as a shipped guide REPLACES it. That is how a client puts
	their own screenshots in front of ours without anyone editing an app.

	A document nobody can open is worse than no document, so private files are excluded
	rather than listed and then refused.
	"""
	files = frappe.get_all(
		"File",
		filters={"folder": TRAINING_FOLDER, "is_folder": 0, "is_private": 0},
		fields=["name", "file_name", "file_url", "file_size", "modified"],
		order_by="file_name asc",
	)

	# Shipped first, so an upload of the same name lands on top of it.
	by_title = {guide["title"]: dict(guide, shipped=True) for guide in _shipped_guides()}

	for f in files:
		name = f.file_name or ""
		# Drop the extension and any leading number used to force the order — the reader
		# wants "Item Transfer", not "02 Item Transfer.pdf".
		title = _readable(name)
		by_title[title] = {
			"title": title,
			"url": f.file_url,
			"is_pdf": name.lower().endswith(".pdf"),
			"size": _file_size(f.file_size),
			"updated": frappe.utils.format_date(f.modified, "d MMM yyyy"),
			"shipped": False,
		}

	return {
		"documents": sorted(by_title.values(), key=lambda d: d["title"].lower()),
		"folder": TRAINING_FOLDER,
		"can_upload": frappe.has_permission("File", "create"),
	}


def _readable(file_name):
	name = file_name.rsplit(".", 1)[0]
	first = name.split(" ", 1)
	if len(first) == 2 and first[0].isdigit():
		name = first[1]
	return name.strip() or file_name


def _file_size(size):
	size = int(size or 0)
	if size >= 1024 * 1024:
		return f"{size / (1024 * 1024):.1f} MB"
	if size >= 1024:
		return f"{round(size / 1024)} KB"
	return f"{size} bytes"


@frappe.whitelist()
def setup():
	"""Re-apply the theme's own site configuration — currently the Stock Control workspace.

	Exists because after_migrate does not reliably fire on a Frappe Cloud deploy, and
	without this repairing that needs bench access.
	"""
	frappe.only_for("System Manager")

	from fuse_theme.install import after_install

	return after_install()
