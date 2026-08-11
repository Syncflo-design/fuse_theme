app_name        = "fuse_theme"
app_title       = "Fuse Theme"
app_publisher   = "Syncflo"
app_description = "Fuse Manufacturing look and feel for Frappe/ERPNext v16 — Sage Intacct inspired, green base."
app_email       = "ops@syncflo.co.za"
app_license     = "MIT"

app_include_css = "fuse_theme.bundle.css"

# Both, because after_migrate has been seen not to fire on a Frappe Cloud deploy — the code
# ships and the configuration that goes with it does not. Also callable as
# fuse_theme.api.setup for the same reason.
after_install = "fuse_theme.install.after_install"
after_migrate = "fuse_theme.install.after_install"

# The v16 desk home is an apps screen, not a workspace list — ERPNext registers Accounting,
# Selling, Stock and the rest there the same way. Without an entry here Fuse is reachable
# only by URL or the workspace sidebar, and the home button always lands somewhere else.
#
# The route goes straight to the Fuse Home page rather than to a workspace: the page IS the
# menu, so stopping at a workspace first would be a click that shows nothing new.
add_to_apps_screen = [
	{
		"name": "fuse_theme",
		"logo": "/assets/fuse_theme/images/fuse-logo.svg",
		"title": "Fuse",
		"route": "/desk/fuse-home",
	}
]

# No home_page / role_home_page hook. Those govern the WEBSITE home page; the desk always
# lands on a workspace, so setting them looked right and changed nothing — the desk kept
# reverting. Reaching a Page is a tile on the workspace, which is how Frappe expects it.
