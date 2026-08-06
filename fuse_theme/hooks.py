app_name        = "fuse_theme"
app_title       = "Fuse Theme"
app_publisher   = "Syncflo"
app_description = "Fuse Manufacturing look and feel for Frappe/ERPNext v16 — Sage Intacct inspired, green base."
app_email       = "ops@syncflo.co.za"
app_license     = "MIT"

app_include_css = "fuse_theme.bundle.css"

# Where "home" goes — the breadcrumb house, /app, and post-login landing.
#
# home_page is the app-wide default: everyone lands on the Fuse page, not the desk
# workspace list. This is a single-product site, so there is no case for dropping a
# user on a generic desk they then have to navigate out of.
#
# role_home_page overrides it per role, for when a role should land somewhere else.
# It is kept for exactly that reason, but note Frappe matches ONE role — a user
# holding several gets whichever the hook resolves first, which is why it cannot be
# the mechanism for the general case.
home_page = "fuse-home"

role_home_page = {
	"Stock Controller": "fuse-home",
}
