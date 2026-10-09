// A permanent way back to Fuse Home from anywhere in the desk: a house beside the title
// of every page.
//
// The desk's own way home is three clicks deep (workspace menu → Apps → Fuse), and v16
// has no top navbar to hang a button on — its header also swallows clicks on controls
// injected into it. Every desk page still draws its own header, so the button goes there.

const FUSE_HOME_ROUTE = '/desk/fuse-home';
const BUTTON_CLASS = 'fuse-home-glyph';

// Lucide "house", inline: no icon font to load and nothing to go stale.
const HOUSE_SVG =
	'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
	'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
	'<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/>' +
	'<path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>' +
	'</svg>';

function build_button() {
	const link = document.createElement('a');
	link.className = BUTTON_CLASS;
	link.href = FUSE_HOME_ROUTE;
	link.title = 'Fuse Home';
	link.setAttribute('aria-label', 'Fuse Home');
	link.innerHTML = HOUSE_SVG;

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

// Every page keeps its own header in the DOM, so rather than work out which one is on
// screen, every header that lacks the button gets one. Fuse Home itself is skipped.
function insert_buttons() {
	document.querySelectorAll('.page-head .page-title').forEach((title) => {
		if (title.querySelector('.' + BUTTON_CLASS)) {
			return;
		}
		if (title.closest('#page-fuse-home, [data-page-route="fuse-home"]')) {
			return;
		}
		const anchor = title.querySelector(':scope > .title-area');
		title.insertBefore(build_button(), anchor || title.firstChild);
	});
}

// A page's header is drawn after its route has changed, sometimes after a server round
// trip for the doctype, so keep looking for a couple of seconds after each navigation.
function place_buttons() {
	insert_buttons();
	let attempts = 0;
	const timer = setInterval(() => {
		attempts += 1;
		insert_buttons();
		if (attempts >= 15) {
			clearInterval(timer);
		}
	}, 200);
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
	place_buttons();
}

if (document.readyState === 'loading') {
	document.addEventListener('DOMContentLoaded', start);
} else {
	start();
}

// Single-page navigation draws a new page's header without a page load, so look again
// after each route change. A header that already has the button is left alone.
if (window.frappe && frappe.router && frappe.router.on) {
	frappe.router.on('change', () => {
		place_buttons();
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
