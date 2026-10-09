app_name        = "fuse_theme"
app_title       = "Fuse Theme"
app_publisher   = "Syncflo"
app_description = "Fuse Manufacturing look and feel for Frappe/ERPNext v16 — Sage Intacct inspired, green base."
app_email       = "ops@syncflo.co.za"
app_license     = "MIT"

app_include_css = "fuse_theme.bundle.css"
app_include_js = "fuse_theme.bundle.js"

# app_include_css reaches the DESK only. The login and password screens are website
# pages, so they need their own include or nothing we write touches them.
web_include_css = "/assets/fuse_theme/css/fuse_web.css"

# Both, because after_migrate has been seen not to fire on a Frappe Cloud deploy — the code
# ships and the configuration that goes with it does not. Also callable as
# fuse_theme.api.setup for the same reason.
after_install = "fuse_theme.install.after_install"
after_migrate = "fuse_theme.install.after_install"

# The user's home (Fuse Home, or their industry's own desk page) and how each app's desk
# shortcuts are drawn, so the desk has both before it paints. See boot.py.
extend_bootinfo = "fuse_theme.boot.extend"

# The v16 desk home is an apps screen, not a workspace list — ERPNext registers Accounting,
# Selling, Stock and the rest there the same way. Without an entry here Fuse is reachable
# only by URL or the workspace sidebar, and the home button always lands somewhere else.
#
# The route goes straight to the Fuse Home page rather than to a workspace: the page IS the
# menu, so stopping at a workspace first would be a click that shows nothing new.
add_to_apps_screen = [
	{
		"name": "fuse_theme",
		# The sphere alone, not the full lockup — the apps screen draws it small and square,
		# so the wordmark would be unreadable at that size.
		"logo": "/assets/fuse_theme/images/fuse-icon.png",
		"title": "Fuse",
		"route": "/desk/fuse-home",
	}
]

# No home_page / role_home_page hook. Those govern the WEBSITE home page; the desk always
# lands on a workspace, so setting them looked right and changed nothing — the desk kept
# reverting. Reaching a Page is a tile on the workspace, which is how Frappe expects it.
