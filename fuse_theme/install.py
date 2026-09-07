"""Site configuration the theme owns.

Wired to after_install AND after_migrate, and exposed as a whitelisted call — on Frappe
Cloud after_migrate has been observed not to fire, shipping code without the configuration
that goes with it. Everything here is idempotent, so re-running only closes gaps.
"""

import json

import frappe

HOME_PAGE = "fuse-home"
TRAINING_PAGE = "fuse-training"
LANDING = "Fuse"
WORKSPACE = "Fuse Stock Control"

# Guides are uploaded here and the Training page reads whatever it finds. One folder, so a
# document can never land somewhere the page does not look.
TRAINING_FOLDER_NAME = "Fuse Training"
TRAINING_FOLDER = f"Home/{TRAINING_FOLDER_NAME}"

# Stock Entry purposes, as the Stock Entry list filters on them. Only these post to
# Intacct — a shortcut to an unfiltered list would invite picking one that does not.
TRANSFER_PURPOSES = ["Material Transfer", "Material Transfer for Manufacture"]

SHORTCUTS = [
	{
		"label": "Transfers",
		"type": "DocType",
		"link_to": "Stock Entry",
		"stats_filter": json.dumps({"purpose": ["in", TRANSFER_PURPOSES]}),
		"color": "Blue",
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
	# Day to day: what is where, what moved, what is coming.
	{"type": "Card Break", "label": "Reports"},
	{"type": "Link", "label": "Stock Balance", "link_type": "Report", "link_to": "Stock Balance",
	 "is_query_report": 1},
	{"type": "Link", "label": "Stock Ledger", "link_type": "Report", "link_to": "Stock Ledger",
	 "is_query_report": 1},
	# Ours, not ERPNext's Stock Projected Qty. Same report and same numbers — it calls
	# theirs — minus the Description column, which is empty on every row because Intacct
	# has nothing that maps onto it.
	{"type": "Link", "label": "Projected Stock", "link_type": "Report",
	 "link_to": "Projected Stock", "is_query_report": 1},
	{"type": "Link", "label": "Warehouse Wise Stock Balance", "link_type": "Report",
	 "link_to": "Warehouse Wise Stock Balance", "is_query_report": 1},
	# Ours, not ERPNext's Purchase Order Analysis. That report is built for a business that
	# receipts and bills in ERPNext; here it does neither, so its Received Qty, Billed
	# Amount and Amount to Bill columns are permanently zero and its chart plots one of
	# them. This shows what is still coming, where it is going and when it was due.
	{"type": "Link", "label": "Stock on Order", "link_type": "Report",
	 "link_to": "Stock on Order", "is_query_report": 1},
	# Planning, from fuse_manufacturing 0.10: the customer order book by item, and the
	# same book netted against stock and exploded through the BOMs into what to make and
	# what to buy. A workspace link to a report that is not installed renders as a dead
	# entry, which is why these ship in the theme only alongside that release.
	{"type": "Link", "label": "Outstanding Orders", "link_type": "Report",
	 "link_to": "Outstanding Orders", "is_query_report": 1},
	{"type": "Link", "label": "Item Demand", "link_type": "Report",
	 "link_to": "Item Demand", "is_query_report": 1},
	# The ones asked at month end or when something looks wrong, kept apart from the daily
	# four so the first card stays scannable.
	{"type": "Card Break", "label": "Analysis"},
	# A Page, not a report — ERPNext calls it Stock Summary and routes it at stock-balance.
	# Given the report of almost the same name sits in the card above, the label matters.
	{"type": "Link", "label": "Stock Summary", "link_type": "Page", "link_to": "stock-balance"},
	{"type": "Link", "label": "Stock Ageing", "link_type": "Report", "link_to": "Stock Ageing",
	 "is_query_report": 1},
	{"type": "Link", "label": "Stock Analytics", "link_type": "Report", "link_to": "Stock Analytics",
	 "is_query_report": 1},
	{"type": "Link", "label": "Item Price Stock", "link_type": "Report",
	 "link_to": "Item Price Stock", "is_query_report": 1},
	{"type": "Card Break", "label": "Master Data"},
	{"type": "Link", "label": "Item", "link_type": "DocType", "link_to": "Item"},
	{"type": "Link", "label": "Warehouse", "link_type": "DocType", "link_to": "Warehouse"},
	{"type": "Link", "label": "BOM", "link_type": "DocType", "link_to": "BOM"},
]

# Every `shortcut_name` must match a SHORTCUTS label and every `card_name` a Card Break
# label in LINKS, exactly — a block naming something that does not exist renders as an
# empty box.
CONTENT = [
	{"id": "fuse_sc_head", "type": "header",
	 "data": {"text": '<span class="h4"><b>Stock Control</b></span>', "col": 12}},
	{"id": "fuse_sc_s1", "type": "shortcut", "data": {"shortcut_name": "Transfers", "col": 4}},
	{"id": "fuse_sc_s3", "type": "shortcut", "data": {"shortcut_name": "Production", "col": 4}},
	{"id": "fuse_sc_c1", "type": "card", "data": {"card_name": "Movements", "col": 3}},
	{"id": "fuse_sc_c2", "type": "card", "data": {"card_name": "Reports", "col": 3}},
	{"id": "fuse_sc_c4", "type": "card", "data": {"card_name": "Analysis", "col": 3}},
	{"id": "fuse_sc_c3", "type": "card", "data": {"card_name": "Master Data", "col": 3}},
]



# ──────────────────────────────────────────────────────────────────────────────
# Quality
# ──────────────────────────────────────────────────────────────────────────────
#
# The home page can only carry a tile or two, and Quality is bigger than that. ERPNext
# ships an entire Quality Management module — procedures, goals, reviews, corrective
# actions, customer feedback — alongside the Quality Inspection that sits in Stock. Two
# tiles reached the inspection list and the template list and nothing else, which made the
# rest look absent when it was only unlinked.
#
# So the Quality tile opens this instead: one place holding everything quality, arranged
# the way the ISO clauses fall rather than the way ERPNext files the doctypes.

QUALITY_WORKSPACE = "Fuse Quality"

QUALITY_SHORTCUTS = [
	{
		"label": "Inspections",
		"type": "DocType",
		"link_to": "Quality Inspection",
		"color": "Blue",
	},
	{
		# The one people actually go looking for. A rejected batch is the reason someone
		# opens this page at all, and finding it should not mean filtering a list first.
		"label": "Rejected",
		"type": "DocType",
		"link_to": "Quality Inspection",
		"stats_filter": json.dumps({"status": "Rejected"}),
		"color": "Red",
	},
	{
		"label": "Procedures",
		"type": "DocType",
		"link_to": "Quality Procedure",
		"color": "Green",
	},
]

QUALITY_LINKS = [
	# 8.6 — releasing what was made, and 7.1.5.2, the instruments the readings came off.
	{"type": "Card Break", "label": "Inspection"},
	{"type": "Link", "label": "Quality Inspection", "link_type": "DocType",
	 "link_to": "Quality Inspection"},
	{"type": "Link", "label": "Quality Inspection Template", "link_type": "DocType",
	 "link_to": "Quality Inspection Template"},
	{"type": "Link", "label": "Quality Inspection Parameter", "link_type": "DocType",
	 "link_to": "Quality Inspection Parameter"},
	{"type": "Link", "label": "Parameter Group", "link_type": "DocType",
	 "link_to": "Quality Inspection Parameter Group"},
	# Ours. A reading is only evidence if the instrument it came off was in calibration,
	# so the register belongs beside the inspections rather than in a corner of its own.
	{"type": "Link", "label": "Measuring Instruments", "link_type": "DocType",
	 "link_to": "Fuse Measuring Instrument"},

	# 7.5 — the documented information itself: how work is done, and what it is aiming at.
	{"type": "Card Break", "label": "Procedures and goals"},
	{"type": "Link", "label": "Quality Procedure", "link_type": "DocType",
	 "link_to": "Quality Procedure"},
	{"type": "Link", "label": "Quality Goal", "link_type": "DocType", "link_to": "Quality Goal"},

	# 9.3 and 8.7 — management review, and what is done about what it finds.
	{"type": "Card Break", "label": "Review and action"},
	{"type": "Link", "label": "Quality Review", "link_type": "DocType", "link_to": "Quality Review"},
	{"type": "Link", "label": "Quality Meeting", "link_type": "DocType",
	 "link_to": "Quality Meeting"},
	{"type": "Link", "label": "Quality Action", "link_type": "DocType", "link_to": "Quality Action"},
	{"type": "Link", "label": "Quality Feedback", "link_type": "DocType",
	 "link_to": "Quality Feedback"},
	{"type": "Link", "label": "Feedback Template", "link_type": "DocType",
	 "link_to": "Quality Feedback Template"},

	# 9.1.2 — the evidence, after the fact.
	{"type": "Card Break", "label": "Reports"},
	{"type": "Link", "label": "Quality Inspection Summary", "link_type": "Report",
	 "link_to": "Quality Inspection Summary", "is_query_report": 1},
	# ERPNext calls this one simply "Review". Labelled by what it reports on, because
	# "Review" on its own says nothing next to Quality Review in the card above.
	{"type": "Link", "label": "Actions Review", "link_type": "Report", "link_to": "Review",
	 "is_query_report": 1},
]

QUALITY_CONTENT = [
	{"id": "fuse_q_head", "type": "header",
	 "data": {"text": '<span class="h4"><b>Quality</b></span>', "col": 12}},
	{"id": "fuse_q_s1", "type": "shortcut", "data": {"shortcut_name": "Inspections", "col": 4}},
	{"id": "fuse_q_s2", "type": "shortcut", "data": {"shortcut_name": "Rejected", "col": 4}},
	{"id": "fuse_q_s3", "type": "shortcut", "data": {"shortcut_name": "Procedures", "col": 4}},
	{"id": "fuse_q_c1", "type": "card", "data": {"card_name": "Inspection", "col": 3}},
	{"id": "fuse_q_c2", "type": "card", "data": {"card_name": "Procedures and goals", "col": 3}},
	{"id": "fuse_q_c3", "type": "card", "data": {"card_name": "Review and action", "col": 3}},
	{"id": "fuse_q_c4", "type": "card", "data": {"card_name": "Reports", "col": 3}},
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


# There is deliberately NO Training workspace.
#
# A workspace called "Fuse Training" derives the route fuse-training, which is also the
# name of the Training page. The workspace then wins every time, so /desk/fuse-training
# opened the workspace and the page could not be reached at all — and saving the workspace
# raised frappe.NameError over the clash.
#
# The page appears in the left menu under Pages on its own, which is what was wanted, so
# the workspace was solving a problem that did not exist.


LOGO = "/assets/fuse_theme/images/fuse-logo.png"
ICON = "/assets/fuse_theme/images/fuse-icon.png"


def _branding():
	"""Put Fuse's own logo on the login screen, the navbar and the browser tab.

	Set here rather than by hand so a new client site is branded on install. The full
	lockup is used only where there is room for the wordmark; everywhere it is drawn small
	and square — navbar, tab, apps screen — it is the sphere on its own.
	"""
	frappe.db.set_single_value(
		"Website Settings",
		{"app_logo": LOGO, "favicon": ICON, "app_name": "Fuse"},
	)
	frappe.db.set_single_value("Navbar Settings", "app_logo", ICON)


def _training_folder():
	"""The folder guides are uploaded into, created if it is not there yet."""
	if frappe.db.exists("File", {"file_name": TRAINING_FOLDER_NAME, "is_folder": 1, "folder": "Home"}):
		return TRAINING_FOLDER

	frappe.get_doc(
		{
			"doctype": "File",
			"file_name": TRAINING_FOLDER_NAME,
			"is_folder": 1,
			"folder": "Home",
		}
	).insert(ignore_permissions=True)
	return TRAINING_FOLDER


def _build(name, title, icon, content, shortcuts, links, sequence_id=None):
	"""Create or refresh one workspace.

	Rebuilt from this definition every time rather than merged: the file is the source of
	truth, so a hand-edit on one site cannot quietly persist and make two clients differ.
	"""
	if frappe.db.exists("Workspace", name):
		doc = frappe.get_doc("Workspace", name)
		doc.shortcuts = []
		doc.links = []
		# Roles too. A leftover role restriction on the hand-made Fuse workspace survived
		# every rebuild because this line was missing, and a workspace the user cannot see
		# is not hidden gracefully — frappe.views.Workspace.show_page gets undefined and
		# throws, taking the sidebar down with it.
		#
		# Fuse workspaces are unrestricted on purpose. What a user may DO is decided by
		# document permissions; hiding the page as well only produces a broken-looking desk.
		doc.roles = []
	else:
		doc = frappe.new_doc("Workspace")
		doc.name = name

	doc.label = name
	doc.title = title
	# Stock, NOT Fuse Theme. A workspace is only in a user's allowed list if they have
	# access to its module, and a non-admin has no documents in Fuse Theme — so the route
	# fell through to a Page lookup and answered "Page fuse-stock-control does not exist".
	# It worked for Administrator, who bypasses all of it, which is why it survived to a
	# client demo on 2026-08-19.
	doc.module = "Stock"
	doc.app = "erpnext"
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


def _set_default_workspace():
	"""Land system users on Fuse rather than wherever the desk would otherwise open.

	Only fills the field where it is EMPTY. Someone who has deliberately chosen a different
	landing workspace keeps it — a setup routine that runs on every migrate must not
	silently undo a user's own preference every time it runs.

	`default_workspace` takes a Workspace, not a Page, so this lands on Fuse and its single
	Fuse Home shortcut. Landing straight on the page is not something the field supports.
	"""
	users = frappe.get_all(
		"User",
		filters={"enabled": 1, "user_type": "System User", "default_workspace": ("in", ("", None))},
		pluck="name",
	)
	for user in users:
		# update_modified=False: this is configuration, not the user editing their profile,
		# and bumping every user's modified stamp on every migrate is noise.
		frappe.db.set_value("User", user, "default_workspace", LANDING, update_modified=False)
	return len(users)


@frappe.whitelist()
def after_install():
	"""Put the site's theme-owned configuration in step with this version of the app.

	Whitelisted so it can be RE-RUN by hand. The module docstring has claimed that since
	this file was written and the decorator was never actually here, which was only found
	when a deploy shipped the Quality workspace and after_migrate did not build it — the
	route answered with the home page and there was no way to close the gap short of
	another deploy.
	"""
	# Only over HTTP. The same function is the after_install and after_migrate hook, where
	# there is no session to check and a refusal would take the whole migrate down.
	if frappe.request:
		frappe.only_for("System Manager")

	landing = _build(
		LANDING, "Fuse", "organization", LANDING_CONTENT, LANDING_SHORTCUTS, [],
		# First in the desk, ahead of ERPNext's own workspaces.
		sequence_id=0,
	)
	stock = _build(WORKSPACE, "Stock Control", "stock", CONTENT, SHORTCUTS, LINKS, sequence_id=1)
	quality = _build(
		QUALITY_WORKSPACE, "Quality", "check", QUALITY_CONTENT, QUALITY_SHORTCUTS,
		QUALITY_LINKS, sequence_id=2,
	)
	_branding()
	folder = _training_folder()
	landed = _set_default_workspace()

	frappe.db.commit()
	return {
		"landing": landing,
		"workspace": stock,
		"quality_workspace": quality,
		"training_page": TRAINING_PAGE,
		"logo": LOGO,
		"training_folder": folder,
		"home_page": HOME_PAGE,
		"shortcuts": len(SHORTCUTS),
		"links": len([link for link in LINKS if link["type"] == "Link"]),
		"users_landed_on_fuse": landed,
	}
