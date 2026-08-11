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
MANUFACTURE = "Manufacture"
TRANSFER = "Material Transfer"
WIP_ISSUE = "Material Transfer for Manufacture"
ADJUSTMENT_PURPOSES = ["Material Receipt", "Material Issue"]

TILES = [
	{
		"key": "works_orders",
		"label": "Works Orders",
		"blurb": "Current manufacturing and production orders",
		"icon": "🔧",
		"route": ["List", "Work Order"],
		"roles": ["Stock Controller", "Manufacturing User", "Manufacturing Manager"],
	},
	{
		"key": "wip_conversion",
		"label": "WIP Conversion",
		"blurb": "Convert raw materials and record output",
		"icon": "📊",
		"route": ["new", "Stock Entry"],
		"options": {"stock_entry_type": MANUFACTURE},
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
		# Deliberately NOT Stock Reconciliation. That is the doctype the opening stock sync
		# uses and it does not post to Intacct — adjusting through it would move stock in
		# ERPNext and leave Intacct none the wiser. Adjustments are Material Receipt (up)
		# and Material Issue (down), so this opens the list and the user picks a direction
		# deliberately rather than having one chosen for them.
		"key": "item_adjustment",
		"label": "Item Adjustment",
		"blurb": "Adjust on-hand quantities in a warehouse",
		"icon": "⚖",
		"route": ["List", "Stock Entry"],
		"options": {"purpose": ["in", ADJUSTMENT_PURPOSES]},
		"roles": ["Stock Controller", "Stock Manager"],
	},
	{
		"key": "stock_control",
		"label": "Stock Control",
		"blurb": "Transfers, adjustments, counts and reports",
		"icon": "📦",
		"route": ["Workspaces", "Fuse Stock Control"],
		"roles": ["Stock Controller", "Stock User", "Stock Manager"],
	},
]


@frappe.whitelist()
def get_home():
	"""Tiles this user may actually use, plus what the header needs.

	Filtered by role AND by read permission on the target doctype — a tile the user
	cannot open is worse than no tile, because it looks like the system is broken
	rather than like they lack access.
	"""
	roles = set(frappe.get_roles())

	tiles = []
	for tile in TILES:
		if not roles.intersection(tile["roles"]):
			continue
		if tile["route"][0] in ("List", "new") and not frappe.has_permission(tile["route"][1], "read"):
			continue
		# A tile that creates something needs create rights, not just read. Otherwise it
		# opens a form the user cannot save, which reads as a broken system rather than as
		# a permission they do not have.
		if tile["route"][0] == "new" and not frappe.has_permission(tile["route"][1], "create"):
			continue
		tiles.append({k: v for k, v in tile.items() if k != "roles"})

	return {
		"tiles": tiles,
		"user": frappe.db.get_value("User", frappe.session.user, "full_name") or frappe.session.user,
		"company": frappe.defaults.get_user_default("Company") or "",
	}


@frappe.whitelist()
def setup():
	"""Re-apply the theme's own site configuration — currently the Stock Control workspace.

	Exists because after_migrate does not reliably fire on a Frappe Cloud deploy, and
	without this repairing that needs bench access.
	"""
	frappe.only_for("System Manager")

	from fuse_theme.install import after_install

	return after_install()
