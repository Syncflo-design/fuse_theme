// A permanent way back to Fuse Home from anywhere in the desk.
//
// The desk's own home button goes to whatever Frappe considers home, which on this stack
// is an apps grid that does not list Fuse. Rather than fight that, the theme puts its own
// button in the navbar. It is ours, so it works the same on every site and every version.

const FUSE_HOME_ROUTE = '/desk/fuse-home';
const BUTTON_ID = 'fuse-home-button';

function build_button() {
	const link = document.createElement('a');
	link.id = BUTTON_ID;
	link.className = 'fuse-home-button';
	link.href = FUSE_HOME_ROUTE;
	link.title = 'Fuse Home';
	link.setAttribute('aria-label', 'Fuse Home');
	link.textContent = 'F';

	// Routed in-app rather than reloading the page, but only on a plain left click —
	// ctrl/cmd/middle click must still open a new tab like any other link.
	link.addEventListener('click', (event) => {
		if (event.metaKey || event.ctrlKey || event.shiftKey || event.button !== 0) {
			return;
		}
		event.preventDefault();
		frappe.set_route('fuse-home');
	});

	return link;
}

function insert_button() {
	if (document.getElementById(BUTTON_ID)) {
		return true;
	}

	// The navbar markup differs between versions, so try the known containers in order
	// rather than depending on one selector surviving an upgrade.
	const host =
		document.querySelector('.navbar .navbar-collapse .navbar-nav.ml-auto') ||
		document.querySelector('.navbar .navbar-nav.ml-auto') ||
		document.querySelector('header .navbar-nav') ||
		document.querySelector('.navbar-nav');

	if (!host) {
		return false;
	}

	const item = document.createElement('li');
	item.className = 'nav-item fuse-home-nav-item';
	item.appendChild(build_button());
	host.insertBefore(item, host.firstChild);
	return true;
}

// The desk root — whatever the user types, and where the home button goes. On v16 /app
// redirects here too, so both are covered.
// /desk/fuse is the landing workspace, which exists only to hold a shortcut to Fuse Home.
// Users land there because default_workspace can point at a Workspace but not at a Page,
// so login sends them one step short of where they are meant to be.
const DESK_ROOTS = ['/desk', '/app', '/desk/fuse', '/app/fuse'];

function at_desk_root() {
	const path = window.location.pathname.replace(/\/+$/, '');
	return DESK_ROOTS.indexOf(path) !== -1;
}

function go_home_if_at_root() {
	if (!at_desk_root()) {
		return;
	}

	// Landing on the desk root shows a workspace grid that does not carry Fuse, and the
	// home button always goes there. Rather than try to change what Frappe considers
	// home — which on this stack is not settable to a Page — the theme claims the root.
	if (window.frappe && frappe.set_route) {
		frappe.set_route('fuse-home');
	} else {
		// replace() rather than assign(), so the grid never enters history and Back does
		// not bounce the user straight back into it.
		window.location.replace('/desk/fuse-home');
	}
}

function start() {
	go_home_if_at_root();

	if (insert_button()) {
		return;
	}

	// The navbar is rendered after boot, and on a slow first load that can be a second or
	// two. Give up after 20 tries rather than observing forever.
	let attempts = 0;
	const timer = setInterval(() => {
		attempts += 1;
		if (insert_button() || attempts > 20) {
			clearInterval(timer);
		}
	}, 250);
}

if (document.readyState === 'loading') {
	document.addEventListener('DOMContentLoaded', start);
} else {
	start();
}

// Single-page navigation replaces parts of the shell, so re-assert the button after each
// route change. insert_button() is a no-op when it is already there.
if (window.frappe && frappe.router && frappe.router.on) {
	frappe.router.on('change', () => {
		insert_button();
		// Also covers the home button, which routes to the desk root in-app without a
		// page load — so the check has to run on every route change, not just at boot.
		go_home_if_at_root();
	});
}

// ---------------------------------------------------------------------------
// Installable on a phone.
//
// Chrome offers "Install app" when the page links a valid manifest over HTTPS.
// Frappe has no hook for adding anything to the desk's <head>, so the links are
// injected here instead — app_include_js runs on every desk page, which is
// exactly the scope the manifest covers.
//
// No service worker. Chrome dropped that requirement for installability, and a
// worker caching desk assets would fight the Frappe Cloud deploy cycle — a
// stale bundle served from a phone's cache is the CDN gotcha with no way to
// clear it. Installed means "own icon, own window", not "works offline": every
// screen posts to Intacct and none of them can work without a connection.
// ---------------------------------------------------------------------------

const MANIFEST_HREF = '/assets/fuse_theme/manifest.json';
const APPLE_ICON_HREF = '/assets/fuse_theme/images/fuse-app-192.png';

function head_link(rel, href, extra) {
	if (document.querySelector('link[rel="' + rel + '"]')) {
		return;
	}
	const link = document.createElement('link');
	link.rel = rel;
	link.href = href;
	Object.assign(link, extra || {});
	document.head.appendChild(link);
}

function install_pwa_head() {
	head_link('manifest', MANIFEST_HREF);

	// iOS ignores the manifest and reads these instead. Safari's "Add to Home
	// Screen" is manual there — there is no prompt to trigger — but the icon and
	// the standalone window come from the meta tags.
	head_link('apple-touch-icon', APPLE_ICON_HREF);

	if (!document.querySelector('meta[name="apple-mobile-web-app-capable"]')) {
		const capable = document.createElement('meta');
		capable.name = 'apple-mobile-web-app-capable';
		capable.content = 'yes';
		document.head.appendChild(capable);
	}

	if (!document.querySelector('meta[name="theme-color"]')) {
		const colour = document.createElement('meta');
		colour.name = 'theme-color';
		colour.content = '#17794a';
		document.head.appendChild(colour);
	}
}

install_pwa_head();
