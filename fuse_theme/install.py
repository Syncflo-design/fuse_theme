"""Site configuration the theme owns.

Wired to after_install AND after_migrate, and exposed as a whitelisted call — on Frappe
Cloud after_migrate has been observed not to fire, shipping code without the configuration
that goes with it. Everything here is idempotent, so re-running only closes gaps.
"""

import json

import frappe

HOME_PAGE = "fuse-home"
LANDING = "Fuse"
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


# The landing workspace. Its only job is to be the way in from the desk: one shortcut to
# the Fuse Home page, which is where the real tiles live.
#
# It used to be maintained by hand and drifted — it still carried an Item Adjustment
# shortcut pointing at Stock Reconciliation, a doctype that does NOT post to Intacct, long
# after that route was removed from the home page. Defined here so it cannot drift again.
LANDING_SHORTCUTS = [
	{"label": "Fuse Home", "type": "Page", "link_to": HOME_PAGE, "color": "Green"},
]

LANDING_CONTENT = [
	{"id": "fuse_land_head", "type": "header",
	 "data": {"text": '<span class="h4"><b>Fuse Manufacturing</b></span>', "col": 12}},
	{"id": "fuse_land_s1", "type": "shortcut", "data": {"shortcut_name": "Fuse Home", "col": 4}},
]


def _build(name, title, icon, content, shortcuts, links, sequence_id=None):
	"""Create or refresh one workspace.

	Rebuilt from this definition every time rather than merged: the file is the source of
	truth, so a hand-edit on one site cannot quietly persist and make two clients differ.
	"""
	if frappe.db.exists("Workspace", name):
		doc = frappe.get_doc("Workspace", name)
		doc.shortcuts = []
		doc.links = []
	else:
		doc = frappe.new_doc("Workspace")
		doc.name = name

	doc.label = name
	doc.title = title
	doc.module = "Fuse Theme"
	doc.icon = icon
	doc.public = 1
	doc.is_hidden = 0
	doc.content = json.dumps(content)
	if sequence_id is not None:
		doc.sequence_id = sequence_id

	for shortcut in shortcuts:
		doc.append("shortcuts", dict(shortcut))
	for link in links:
		doc.append("links", dict(link))

	doc.flags.ignore_permissions = True
	doc.flags.ignore_links = True
	doc.save(ignore_permissions=True)
	return doc.name


def after_install():
	"""Put the site's theme-owned configuration in step with this version of the app."""
	landing = _build(
		LANDING, "Fuse", "organization", LANDING_CONTENT, LANDING_SHORTCUTS, [],
		# First in the desk, ahead of ERPNext's own workspaces.
		sequence_id=0,
	)
	stock = _build(WORKSPACE, "Stock Control", "stock", CONTENT, SHORTCUTS, LINKS, sequence_id=1)

	frappe.db.commit()
	return {
		"landing": landing,
		"workspace": stock,
		"home_page": HOME_PAGE,
		"shortcuts": len(SHORTCUTS),
		"links": len([link for link in LINKS if link["type"] == "Link"]),
	}
