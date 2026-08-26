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

const BUILD_MARKER = 'v0.8.1-2026-08-25-footer-extras';

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
			'  <img class="fuse-home__mark" src="/assets/fuse_theme/images/fuse-icon.png" alt="Fuse">',
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
			'</div>',
			'<div class="fuse-home__footer" data-fuse="footer"></div>'
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
				this.render_footer(data.floor, data.training, data.extras);
			})
			.catch((e) => this.render_error(e));
	}

	// The phone screens, below the fold of the modules people work in all day.
	//
	// Same card language as a tile — icon chip, title, blurb, chevron — at a
	// smaller scale and without the green top rule, so it reads as related but
	// subordinate rather than as a tile someone forgot to align. The real way in
	// is the installed app; this is how you show it from a desk.
	render_footer(floor, training, extras) {
		const $footer = this.$root.find('[data-fuse="footer"]');
		$footer.empty();
		extras = extras || [];
		if ((!floor || !floor.route) && (!training || !training.route) && !extras.length) return;

		// Inline SVG (Lucide "smartphone"), not an emoji: an emoji cannot take a
		// colour from the stylesheet and renders differently on every platform.
		const icon =
			'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
			'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' +
			'<rect x="5" y="2" width="14" height="20" rx="2"></rect><path d="M12 18h.01"></path></svg>';

		const chevron =
			'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
			'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' +
			'<path d="M9 18l6-6-6-6"></path></svg>';

		const $card = $(
			'<button type="button" class="fuse-home__floor">' +
			'  <span class="fuse-home__floor-icon">' + icon + '</span>' +
			'  <span class="fuse-home__floor-body">' +
			'    <span class="fuse-home__floor-label"></span>' +
			'    <span class="fuse-home__floor-blurb">Scan, count and confirm on a phone or tablet</span>' +
			'  </span>' +
			'  <span class="fuse-home__floor-chevron">' + chevron + '</span>' +
			'</button>'
		);

		// .text(), not markup — the label is data from the server.
		$card.find('.fuse-home__floor-label').text(floor.label || 'Shop floor');
		$card.on('click', () => frappe.set_route(floor.route));

		$footer.append('<div class="fuse-home__heading">Also here</div>');
		if (floor && floor.route) $footer.append($card);

		// The guides. Same card, a book instead of a phone — help belongs where people
		// already are, not behind a menu they have to be told about.
		if (training && training.route) {
			const book =
				'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
				'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' +
				'<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>' +
				'<path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>';

			const $guides = $(
				'<button type="button" class="fuse-home__floor">' +
				'  <span class="fuse-home__floor-icon">' + book + '</span>' +
				'  <span class="fuse-home__floor-body">' +
				'    <span class="fuse-home__floor-label"></span>' +
				'    <span class="fuse-home__floor-blurb">How to do each of these, step by step</span>' +
				'  </span>' +
				'  <span class="fuse-home__floor-chevron">' + chevron + '</span>' +
				'</button>'
			);
			$guides.find('.fuse-home__floor-label').text(training.label || 'Guides');
			$guides.on('click', () => frappe.set_route(training.route));
			$footer.append($guides);
		}

		// Anything an app has asked to sit on this row. Same card again, so a contributed
		// one is indistinguishable from the two above — the row is a row, not a place
		// where the built-in cards look different from everybody else's.
		extras.forEach((tile) => {
			// A contributed tile may carry its own SVG path. Preferred over its emoji for
			// the same reason the two above use one: an emoji cannot take a colour from
			// the stylesheet and renders differently on every platform.
			const mark = tile.svg
				? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
				  'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" ' +
				  'focusable="false">' + tile.svg + '</svg>'
				: '';

			const $extra = $(
				'<button type="button" class="fuse-home__floor">' +
				'  <span class="fuse-home__floor-icon"></span>' +
				'  <span class="fuse-home__floor-body">' +
				'    <span class="fuse-home__floor-label"></span>' +
				'    <span class="fuse-home__floor-blurb"></span>' +
				'  </span>' +
				'  <span class="fuse-home__floor-chevron">' + chevron + '</span>' +
				'</button>'
			);

			// .text() for anything from the server, .html() only for the SVG we built here.
			if (mark) {
				$extra.find('.fuse-home__floor-icon').html(mark);
			} else {
				$extra.find('.fuse-home__floor-icon').text(tile.icon || '');
			}
			$extra.find('.fuse-home__floor-label').text(tile.label || '');
			$extra.find('.fuse-home__floor-blurb').text(tile.blurb || '');
			// go(), the same opener the tiles use — a footer card pointing at a new
			// document needs frappe.new_doc() rather than set_route, and that logic
			// belongs in one place.
			$extra.on('click', () => this.go(tile));
			$footer.append($extra);
		});
	}

	render_subtitle(data) {
		const bits = [];
		if (data.user) bits.push(data.user);
		if (data.company) bits.push(data.company);
		const text = bits.length ? bits.join(' · ') : 'Choose a module to get started.';
		this.$root.find('[data-fuse="subtitle"]').text(text);
	}

	// Open whatever a tile or a choice points at.
	//
	// route_options is Frappe's own mechanism and covers both cases: filters on a List
	// route, field defaults on a new document. Set immediately before navigating so
	// nothing else can consume it first — Frappe clears it on use.
	go(target) {
		if (target.options) {
			frappe.route_options = Object.assign({}, target.options);
		}

		// A new document is NOT a route. set_route('new', 'Stock Entry') builds
		// /desk/new/Stock%20Entry, which v16 answers with "Page new not found" —
		// frappe.new_doc() is the only way in, and it still honours route_options.
		if (target.route[0] === 'new') {
			frappe.new_doc(target.route[1]);
			return;
		}

		frappe.set_route.apply(null, target.route);
	}

	// Ask which way before opening anything.
	//
	// Used by Item Adjustment, where the direction is the whole decision: an adjustment
	// posts to Intacct on submit, so picking the wrong one is not something you quietly
	// correct afterwards.
	ask(tile) {
		const dialog = new frappe.ui.Dialog({ title: tile.label });
		const $body = $(dialog.body).empty().addClass('fuse-choices');

		tile.choices.forEach((choice) => {
			const $button = $(
				'<button type="button" class="fuse-choice">' +
					'  <span class="fuse-choice__label"></span>' +
					'  <span class="fuse-choice__blurb"></span>' +
					'</button>'
			);
			// .text() again — a choice label is data from the server, not markup.
			$button.find('.fuse-choice__label').text(choice.label || '');
			$button.find('.fuse-choice__blurb').text(choice.blurb || '');
			$button.on('click', () => {
				dialog.hide();
				this.go(choice);
			});
			$body.append($button);
		});

		dialog.show();
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

		// Two rows, not one run. Everything without a group is a step that moves stock —
		// receive, plan, make, move. What carries `group` does not: a request for material,
		// the BOM a job is built from, the project it is booked against. Same card, own
		// grid, a rule between, so the eye stops rather than counting nine equal things.
		// Ordered explicitly, because the natural order puts every contributed tile after
		// every built-in one — an app's tile would always land last just because its app is
		// read last, which is not a decision anybody made.
		const reference = tiles
			.filter((t) => t.group)
			.sort((a, b) => (a.order || 0) - (b.order || 0));

		const $grid = $('<div class="fuse-home__grid"></div>').appendTo($tiles);
		let $second = null;
		if (reference.length) {
			$second = $('<div class="fuse-home__grid fuse-home__grid--reference"></div>');
		}

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
			$tile.on('click', () => {
				if (tile.choices && tile.choices.length) {
					this.ask(tile);
					return;
				}
				this.go(tile);
			});

			(tile.group ? $second : $grid).append($tile);
		});

		// Appended after the loop so the reference row always lands below the actions,
		// whatever order the apps contributed their tiles in.
		if ($second) $tiles.append($second);
	}

	render_error(e) {
		const message = (e && e.message) || 'Could not load the dashboard.';
		this.$root
			.find('[data-fuse="tiles"]')
			.html($('<div class="fuse-home__error">').text(message));
	}
}
