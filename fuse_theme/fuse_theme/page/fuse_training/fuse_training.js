// Training & Help — the guides, read in the browser.
//
// Driven entirely by what is in the Fuse Training folder. Nothing about a document is
// hardcoded here, so replacing a guide is an upload and nothing else: no code change, no
// deploy, and the list picks it up on the next refresh.
//
// fuse-training/<folder> shows one other folder under Home the same way — a site's own
// documents, such as the demo site's Demo Pack — without the desk's list sidebars.

const BUILD_MARKER = 'v0.3.0-2026-10-08-folder-view';

frappe.pages['fuse-training'].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Training & Help',
		single_column: true,
	});
	wrapper.fuse_training = new FuseTraining(page);
};

// The page is built once and then reused, so moving between the guides and a folder
// arrives here rather than at on_page_load. Reload only when the folder has changed —
// the first show follows straight on from the load above.
frappe.pages['fuse-training'].on_page_show = function (wrapper) {
	const view = wrapper.fuse_training;
	if (view && view.folder !== view.route_folder()) {
		view.load();
	}
};

class FuseTraining {
	constructor(page) {
		this.page = page;
		this.$root = $(page.main);
		this.load();

		this.page.set_primary_action('Refresh', () => this.load(), 'refresh');
	}

	// The folder named after the page in the route, or '' for the guides themselves.
	route_folder() {
		return frappe.get_route()[1] || '';
	}

	render_shell() {
		this.$root.html(`
			<div class="fuse-training">
				<div class="fuse-training__intro">
					<h2 class="fuse-training__heading"></h2>
					<p class="fuse-training__blurb"></p>
				</div>
				<div data-fuse="upload"></div>
				<div data-fuse="docs" class="fuse-training__list">
					<div class="fuse-training__empty">Loading…</div>
				</div>
			</div>
		`);

		// Through .text(): the folder name comes from the URL and is data, not markup.
		this.page.set_title(this.folder || 'Training & Help');
		this.$root.find('.fuse-training__heading').text(this.folder || 'Fuse guides');
		this.$root.find('.fuse-training__blurb').text(
			this.folder
				? 'Documents kept on this site. Click one to read it — it opens in a new tab.'
				: 'Step-by-step guides for each job in Fuse. Click one to read it — it opens in a ' +
				  'new tab, so you can keep it beside you while you work.'
		);
	}

	load() {
		this.folder = this.route_folder();
		this.render_shell();
		frappe
			.call({
				method: 'fuse_theme.api.get_training_documents',
				args: this.folder ? { folder: this.folder } : {},
			})
			.then((r) => this.render(r.message || {}))
			.catch((e) => this.render_error(e));
	}

	render(data) {
		this.render_upload(data.can_upload, data.folder);

		const $list = this.$root.find('[data-fuse="docs"]').empty();
		const docs = data.documents || [];

		if (!docs.length) {
			const none = this.folder ? 'Nothing has been added to this folder yet.' : 'No guides have been uploaded yet.';
			const next = data.can_upload
				? `Use ${this.upload_label()} above to add the first one.`
				: 'Ask your administrator to add them.';
			$list.html($('<div class="fuse-training__empty"></div>').text(`${none} ${next}`));
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
			// A shipped guide has no size or date — it is an app asset, not a File record.
			// Interpolating them regardless printed "undefined · updated undefined" under
			// every guide the app ships, which is most of them.
			const meta = [doc.size, doc.updated && `updated ${doc.updated}`].filter(Boolean);
			$card.find('.fuse-doc__meta').text(meta.join(' · '));
			$list.append($card);
		});
	}

	upload_label() {
		return this.folder ? 'Upload a document' : 'Upload a guide';
	}

	render_upload(can_upload, folder) {
		const $slot = this.$root.find('[data-fuse="upload"]').empty();
		if (!can_upload) {
			return;
		}

		const $btn = $('<button type="button" class="btn btn-default btn-sm fuse-training__upload"></button>');
		$btn.text(this.upload_label());
		$btn.on('click', () => {
			new frappe.ui.FileUploader({
				// Straight into the folder this page is showing, so a document never lands
				// somewhere the page cannot see it.
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
		const message = (e && e.message) || 'Could not load the documents.';
		this.$root.find('[data-fuse="docs"]').html(
			$('<div class="fuse-training__empty"></div>').text(message)
		);
	}
}
