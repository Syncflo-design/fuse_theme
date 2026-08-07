app_name        = "fuse_theme"
app_title       = "Fuse Theme"
app_publisher   = "Syncflo"
app_description = "Fuse Manufacturing look and feel for Frappe/ERPNext v16 — Sage Intacct inspired, green base."
app_email       = "ops@syncflo.co.za"
app_license     = "MIT"

app_include_css = "fuse_theme.bundle.css"

# No home_page / role_home_page hook. Those govern the WEBSITE home page; the desk always
# lands on a workspace, so setting them looked right and changed nothing — the desk kept
# reverting. Reaching a Page is a tile on the workspace, which is how Frappe expects it.
