"""Site configuration the theme owns.

Wired to after_install AND after_migrate, and exposed as a whitelisted call — on Frappe
Cloud after_migrate has been observed not to fire, shipping code without the configuration
that goes with it. Everything here is idempotent, so re-running only closes gaps.
"""

import json

import frappe

WORKSPACE = "Fuse Stock Control"

# Stock Entry purposes, as the Stock Entry list filters on them. Only these post to
# Intacct — a shortcut to an unfiltered list would invite picking one that does not.
TRANSFER_PURPOSES = ["Material Transfer", "Material Transfer for Manufacture"]
ADJUSTMENT_PURPOSES = ["Material Receipt", "Material Issue"]

SHORTCUTS = [
	{
		"label": "Transfers",
		"type": "DocType",
		"link_to": "Stock Entry",
		"stats_filter": json.dumps({"purpose": ["in", TRANSFER_PURPOSES]}),
		"color": "Blue",
	},
	{
		"label": "Adjustments",
		"type": "DocType",
		"link_to": "Stock Entry",
		"stats_filter": json.dumps({"purpose": ["in", ADJUSTMENT_PURPOSES]}),
		"color": "Orange",
	},
	{
		"label": "Production",
		"type": "DocType",
		"link_to": "Stock Entry",
		"stats_filter": json.dumps({"purpose": "Manufacture"}),
		"color": "Green",
	},
]

# Card Break rows open a card; the Link rows after it belong to that card.
LINKS = [
	{"type": "Card Break", "label": "Movements"},
	{"type": "Link", "label": "Stock Entry", "link_type": "DocType", "link_to": "Stock Entry"},
	{"type": "Link", "label": "Work Order", "link_type": "DocType", "link_to": "Work Order"},
	{"type": "Card Break", "label": "Reports"},
	{"type": "Link", "label": "Stock Balance", "link_type": "Report", "link_to": "Stock Balance",
	 "is_query_report": 1},
	{"type": "Link", "label": "Stock Ledger", "link_type": "Report", "link_to": "Stock Ledger",
	 "is_query_report": 1},
	{"type": "Link", "label": "Stock Projected Qty", "link_type": "Report",
	 "link_to": "Stock Projected Qty", "is_query_report": 1},
	{"type": "Card Break", "label": "Master Data"},
	{"type": "Link", "label": "Item", "link_type": "DocType", "link_to": "Item"},
	{"type": "Link", "label": "Warehouse", "link_type": "DocType", "link_to": "Warehouse"},
]

CONTENT = [
	{"id": "fuse_sc_head", "type": "header",
	 "data": {"text": '<span class="h4"><b>Stock Control</b></span>', "col": 12}},
	{"id": "fuse_sc_s1", "type": "shortcut", "data": {"shortcut_name": "Transfers", "col": 4}},
	{"id": "fuse_sc_s2", "type": "shortcut", "data": {"shortcut_name": "Adjustments", "col": 4}},
	{"id": "fuse_sc_s3", "type": "shortcut", "data": {"shortcut_name": "Production", "col": 4}},
	{"id": "fuse_sc_c1", "type": "card", "data": {"card_name": "Movements", "col": 4}},
	{"id": "fuse_sc_c2", "type": "card", "data": {"card_name": "Reports", "col": 4}},
	{"id": "fuse_sc_c3", "type": "card", "data": {"card_name": "Master Data", "col": 4}},
]


def _build_workspace():
	"""Create or refresh the Stock Control workspace.

	Rebuilt from this definition every time rather than merged: the file is the source of
	truth, so a hand-edit on one site cannot quietly persist and make two clients differ.
	"""
	if frappe.db.exists("Workspace", WORKSPACE):
		doc = frappe.get_doc("Workspace", WORKSPACE)
		doc.shortcuts = []
		doc.links = []
	else:
		doc = frappe.new_doc("Workspace")
		doc.name = WORKSPACE

	doc.label = WORKSPACE
	doc.title = "Stock Control"
	doc.module = "Fuse Theme"
	doc.icon = "stock"
	doc.public = 1
	doc.is_hidden = 0
	doc.content = json.dumps(CONTENT)

	for shortcut in SHORTCUTS:
		doc.append("shortcuts", dict(shortcut))
	for link in LINKS:
		doc.append("links", dict(link))

	doc.flags.ignore_permissions = True
	doc.flags.ignore_links = True
	doc.save(ignore_permissions=True)
	return doc.name


def after_install():
	"""Put the site's theme-owned configuration in step with this version of the app."""
	name = _build_workspace()
	frappe.db.commit()
	return {
		"workspace": name,
		"shortcuts": len(SHORTCUTS),
		"links": len([link for link in LINKS if link["type"] == "Link"]),
	}
