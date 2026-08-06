app_name        = "fuse_theme"
app_title       = "Fuse Theme"
app_publisher   = "Syncflo"
app_description = "Fuse Manufacturing look and feel for Frappe/ERPNext v16 — Sage Intacct inspired, green base."
app_email       = "ops@syncflo.co.za"
app_license     = "MIT"

app_include_css = "fuse_theme.bundle.css"

# Land the stock controller on the Fuse page rather than a workspace. Frappe's
# per-user workspace API is not a reliable target, so this uses the documented
# role_home_page hook, which desk honours.
role_home_page = {
	"Stock Controller": "fuse-home",
}
