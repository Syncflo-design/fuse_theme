// ============================================================================
// fuse_home.js — the Fuse landing page
//
// Bump BUILD_MARKER every deploy. It is the only reliable way to tell whether
// Frappe Cloud actually rebuilt assets or served the cached bundle.
//
// Pattern rules, learned the hard way and not to be "tidied":
//   1. HTML is a string ARRAY joined with newlines, never a template literal.
//   2. fuse_home.html is a placeholder only — Frappe registers it as a
//      single-quoted template, so an apostrophe in it breaks the page.
//   3. Mount into page.body via $('<div>').appendTo(page.body). Do NOT reach
//      for $(wrapper).find(...) — the v16 Page API does not guarantee it.
//   4. CSS lives in its own file, linked from here, so this stays small.
// ============================================================================

const BUILD_MARKER = 'v0.1.0-2026-08-06-fuse-home';

frappe.pages['fuse-home'].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Fuse',
		single_column: true
	});

	window.fuseHome = new FuseHome(page);
};

frappe.pages['fuse-home'].on_page_show = function () {
	if (window.fuseHome) {
		window.fuseHome.refresh();
	}
};

class FuseHome {
	constructor(page) {
		this.page = page;
		this.load_css();

		this.$root = $('<div class="fuse-home">').appendTo(this.page.body);

		this.page.set_secondary_action('Refresh', () => this.refresh(), 'refresh');

		this.render_shell();
		this.refresh();
	}

	load_css() {
		const href = '/assets/fuse_theme/css/fuse_home.css';
		if (!document.querySelector('link[href^="' + href + '"]')) {
			$('<link rel="stylesheet" type="text/css">')
				.attr('href', href + '?v=' + encodeURIComponent(BUILD_MARKER))
				.appendTo('head');
		}
	}

	render_shell() {
		const html = [
			'<div class="fuse-home__banner">',
			'  <div class="fuse-home__mark">F</div>',
			'  <div class="fuse-home__titles">',
			'    <div class="fuse-home__title">Fuse Manufacturing</div>',
			'    <div class="fuse-home__subtitle" data-fuse="subtitle">Loading...</div>',
			'  </div>',
			'  <div class="fuse-home__clock">',
			'    <div class="fuse-home__time" data-fuse="time"></div>',
			'    <div class="fuse-home__date" data-fuse="date"></div>',
			'  </div>',
			'</div>',
			'<div class="fuse-home__heading">Quick Launch</div>',
			'<div class="fuse-home__tiles" data-fuse="tiles">',
			'  <div class="fuse-home__skeleton"></div>',
			'  <div class="fuse-home__skeleton"></div>',
			'  <div class="fuse-home__skeleton"></div>',
			'</div>'
		].join('\n');

		this.$root.html(html);
		this.start_clock();
	}

	start_clock() {
		const paint = () => {
			const now = frappe.datetime.now_datetime();
			const time = now.slice(11, 16);
			const date = frappe.datetime.str_to_user(now.slice(0, 10));
			this.$root.find('[data-fuse="time"]').text(time);
			this.$root.find('[data-fuse="date"]').text(date);
		};
		paint();
		// Cleared on page change by Frappe tearing down the wrapper; a minute is
		// coarse enough that drift never shows.
		if (this.clock) clearInterval(this.clock);
		this.clock = setInterval(paint, 60000);
	}

	refresh() {
		frappe
			.call({ method: 'fuse_theme.api.get_home' })
			.then((r) => {
				const data = (r && r.message) || {};
				this.render_subtitle(data);
				this.render_tiles(data.tiles || []);
			})
			.catch((e) => this.render_error(e));
	}

	render_subtitle(data) {
		const bits = [];
		if (data.user) bits.push(data.user);
		if (data.company) bits.push(data.company);
		const text = bits.length ? bits.join(' · ') : 'Choose a module to get started.';
		this.$root.find('[data-fuse="subtitle"]').text(text);
	}

	render_tiles(tiles) {
		const $tiles = this.$root.find('[data-fuse="tiles"]');

		if (!tiles.length) {
			$tiles.html(
				'<div class="fuse-home__empty">Nothing available to you here yet. ' +
					'Ask an administrator to check your roles.</div>'
			);
			return;
		}

		$tiles.empty();

		tiles.forEach((tile) => {
			const html = [
				'<button type="button" class="fuse-tile">',
				'  <span class="fuse-tile__icon"></span>',
				'  <span class="fuse-tile__body">',
				'    <span class="fuse-tile__label"></span>',
				'    <span class="fuse-tile__blurb"></span>',
				'  </span>',
				'  <span class="fuse-tile__chevron">&rsaquo;</span>',
				'</button>'
			].join('\n');

			// Text is set through .text(), never interpolated into the markup —
			// a tile label is data and must not be able to inject HTML.
			const $tile = $(html);
			$tile.find('.fuse-tile__icon').text(tile.icon || '');
			$tile.find('.fuse-tile__label').text(tile.label || '');
			$tile.find('.fuse-tile__blurb').text(tile.blurb || '');
			$tile.on('click', () => frappe.set_route.apply(null, tile.route));

			$tiles.append($tile);
		});
	}

	render_error(e) {
		const message = (e && e.message) || 'Could not load the dashboard.';
		this.$root
			.find('[data-fuse="tiles"]')
			.html($('<div class="fuse-home__error">').text(message));
	}
}
