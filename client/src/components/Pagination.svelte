<script>
	export let totalCount = 0; // Total number of items (passed from parent)
	export let itemsPerPage = 10; // Number of items per page
	export let currentPage = 1; // Current active page (bindable)
	export let onPageChange; // Callback function for page changes

	// Calculate total pages
	let totalPages = Math.ceil(totalCount / itemsPerPage);

	// Generate the pagination range
	$: pagination = generatePagination(currentPage, totalPages);

	// Function to generate pagination numbers
	function generatePagination(current, total) {
		const visiblePages = 5; // Maximum visible pages
		let pages = [];

		if (total <= visiblePages) {
			// Show all pages if the total number of pages is small
			for (let i = 1; i <= total; i++) {
				pages.push(i);
			}
		} else {
			// Always include the first page
			pages.push(1);

			// Add dots if we're past page 3
			if (current > 3) {
				pages.push('...');
			}

			// Add middle pages
			for (let i = Math.max(2, current - 1); i <= Math.min(total - 1, current + 1); i++) {
				pages.push(i);
			}

			// Add dots if we're before the second-to-last page
			if (current < total - 2) {
				pages.push('...');
			}

			// Always include the last page
			pages.push(total);
		}

		return pages;
	}

	// Handle page change
	function handlePageChange(page) {
		if (page === '...' || page === currentPage) return; // Ignore invalid or same-page clicks
		currentPage = page; // Update the currentPage prop
		onPageChange && onPageChange(page); // Trigger the parent callback
	}
</script>

<div class="flex justify-between items-center">
	<!-- Pagination Links -->
	<div class="pagination flex items-center space-x-2">
		<!-- Previous Button -->
		<button
			on:click={() => handlePageChange(currentPage - 1)}
			disabled={currentPage === 1}
			class="px-3 py-1 rounded bg-[var(--color-bg-2)] text-[var(--color-text-muted)] hover:text-[var(--color-accent)] disabled:opacity-50">
			Previous
		</button>

		<!-- Page Numbers -->
		{#each pagination as page}
			<button
				on:click={() => handlePageChange(page)}
				class="px-3 py-1 rounded bg-[var(--color-bg-2)] text-[var(--color-text-muted)] hover:text-[var(--color-accent)] {page === currentPage ? 'font-bold bg-[var(--color-bg-1)]' : ''}">
				{page}
			</button>
		{/each}

		<!-- Next Button -->
		<button
			on:click={() => handlePageChange(currentPage + 1)}
			disabled={currentPage >= totalPages}
			class="px-3 py-1 rounded bg-[var(--color-bg-2)] text-[var(--color-text-muted)] hover:text-[var(--color-accent)] disabled:opacity-50">
			Next
		</button>
	</div>

	<!-- Total Count Section -->
	<div class="flex items-center space-x-2 text-[var(--color-accent)] font-bold bg-[var(--color-bg-2)] rounded-lg px-4 py-2 shadow-md">
		<span>Total: {totalCount} items</span>
	</div>
</div>
