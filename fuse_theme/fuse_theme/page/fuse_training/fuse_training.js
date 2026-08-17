// Training & Help — the guides, read in the browser.
//
// Driven entirely by what is in the Fuse Training folder. Nothing about a document is
// hardcoded here, so replacing a guide is an upload and nothing else: no code change, no
// deploy, and the list picks it up on the next refresh.

const BUILD_MARKER = 'v0.2.0-2026-08-17-logo-and-redirect';

frappe.pages['fuse-training'].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Training & Help',
		single_column: true,
	});
	new FuseTraining(page);
};

class FuseTraining {
	constructor(page) {
		this.page = page;
		this.$root = $(page.main);
		this.render_shell();
		this.load();

		this.page.set_primary_action('Refresh', () => this.load(), 'refresh');
	}

	render_shell() {
		this.$root.html(`
			<div class="fuse-training">
				<div class="fuse-training__intro">
					<h2 class="fuse-training__heading">Fuse guides</h2>
					<p class="fuse-training__blurb">
						Step-by-step guides for each job in Fuse. Click one to read it — it opens in a
						new tab, so you can keep it beside you while you work.
					</p>
				</div>
				<div data-fuse="upload"></div>
				<div data-fuse="docs" class="fuse-training__list">
					<div class="fuse-training__empty">Loading…</div>
				</div>
			</div>
		`);
	}

	load() {
		frappe
			.call({ method: 'fuse_theme.api.get_training_documents' })
			.then((r) => this.render(r.message || {}))
			.catch((e) => this.render_error(e));
	}

	render(data) {
		this.render_upload(data.can_upload, data.folder);

		const $list = this.$root.find('[data-fuse="docs"]').empty();
		const docs = data.documents || [];

		if (!docs.length) {
			$list.html(`
				<div class="fuse-training__empty">
					No guides have been uploaded yet.
					${data.can_upload ? 'Use Upload a guide above to add the first one.' : 'Ask your administrator to add them.'}
				</div>
			`);
			return;
		}

		docs.forEach((doc) => {
			// Text through .text(), never interpolated — a file name is data and must not be
			// able to inject markup into the page.
			const $card = $(`
				<a class="fuse-doc" target="_blank" rel="noopener">
					<span class="fuse-doc__icon"></span>
					<span class="fuse-doc__body">
						<span class="fuse-doc__title"></span>
						<span class="fuse-doc__meta"></span>
					</span>
					<span class="fuse-doc__open">Open</span>
				</a>
			`);
			$card.attr('href', doc.url);
			$card.find('.fuse-doc__icon').text(doc.is_pdf ? '📄' : '📎');
			$card.find('.fuse-doc__title').text(doc.title);
			$card.find('.fuse-doc__meta').text(`${doc.size} · updated ${doc.updated}`);
			$list.append($card);
		});
	}

	render_upload(can_upload, folder) {
		const $slot = this.$root.find('[data-fuse="upload"]').empty();
		if (!can_upload) {
			return;
		}

		const $btn = $('<button type="button" class="btn btn-default btn-sm fuse-training__upload">Upload a guide</button>');
		$btn.on('click', () => {
			new frappe.ui.FileUploader({
				// Straight into the training folder, so a document never lands somewhere the
				// page cannot see it.
				folder: folder,
				disable_file_browser: true,
				on_success: () => {
					frappe.show_alert({ message: 'Uploaded', indicator: 'green' });
					this.load();
				},
			});
		});
		$slot.append($btn);
	}

	render_error(e) {
		const message = (e && e.message) || 'Could not load the guides.';
		this.$root.find('[data-fuse="docs"]').html(
			$('<div class="fuse-training__empty"></div>').text(message)
		);
	}
}
