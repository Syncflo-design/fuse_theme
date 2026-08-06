"""Data for the Fuse home page.

One whitelisted call returns everything the page paints. Tiles are declared here
rather than in a DocType: there is one product, one tile set, and a record-driven
tile library is only worth its weight once admins need to add tiles themselves.

Each tile's `route` is a frappe.set_route argument array.
"""

import frappe

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
		"route": ["List", "Stock Entry"],
		"roles": ["Stock Controller", "Manufacturing User", "Manufacturing Manager"],
	},
	{
		"key": "quick_transfer",
		"label": "Quick Item Transfer",
		"blurb": "Move one item between warehouses",
		"icon": "⇄",
		"route": ["new", "Stock Entry"],
		"roles": ["Stock Controller", "Stock User", "Stock Manager"],
	},
	{
		"key": "bulk_transfer",
		"label": "Bulk Item Transfer",
		"blurb": "Move several items on one transfer slip",
		"icon": "⤫",
		"route": ["List", "Stock Entry"],
		"roles": ["Stock Controller", "Stock User", "Stock Manager"],
	},
	{
		"key": "item_adjustment",
		"label": "Item Adjustment",
		"blurb": "Adjust on-hand quantities in a warehouse",
		"icon": "⚖",
		"route": ["List", "Stock Reconciliation"],
		"roles": ["Stock Controller", "Stock Manager"],
	},
	{
		"key": "stock_control",
		"label": "Stock Control",
		"blurb": "Transfers, adjustments, counts and reports",
		"icon": "📦",
		"route": ["query-report", "Stock Balance"],
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
		tiles.append({k: v for k, v in tile.items() if k != "roles"})

	return {
		"tiles": tiles,
		"user": frappe.db.get_value("User", frappe.session.user, "full_name") or frappe.session.user,
		"company": frappe.defaults.get_user_default("Company") or "",
	}
