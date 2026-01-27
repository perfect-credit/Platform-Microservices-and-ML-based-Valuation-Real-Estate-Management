<script>
	import { user } from '../stores/auth.js';
	import { onMount } from 'svelte';
	import Card from '../components/Card.svelte';
	import Pagination from '../components/Pagination.svelte';

	let properties = []; // Array of properties to display
	let currentPage = 1; // Current active page
	const itemsPerPage = 20; // Number of items per page
	let totalCount = 0; // Total number of properties (fetched dynamically)

	let userDetails;
	$: userDetails = $user; // Reactive store subscription

	let loading = true; // Loading state for the page

	async function fetchProperties() {
		if (!userDetails || !userDetails.token) {
			console.error('No token available. Please log in.');
			return;
		}

		try {
			loading = true;
			let url = 'http://localhost:8000/api/v1/spm/properties';
			if (currentPage > 1) {
				url += `?page=${currentPage}`;
			}

			const response = await fetch(url, {
				method: 'GET',
				headers: {
					Authorization: `${userDetails.token}`, // Include token in the Authorization header
					'Content-Type': 'application/json',
				},
			});

			if (response.ok) {
				const data = await response.json();
				properties = data;
			} else {
				console.error('Failed request:', response.status);
			}
		} catch (error) {
			console.error('Error making request:', error);
		} finally {
			loading = false;
		}
	}

	async function fetchTotalCount() {
		if (!userDetails || !userDetails.token) {
			console.error('No token available. Please log in.');
			return;
		}

		try {
			const response = await fetch('http://localhost:8000/api/v1/spm/properties/count', {
				method: 'GET',
				headers: {
					Authorization: `${userDetails.token}`, // Include token in the Authorization header
					'Content-Type': 'application/json',
				},
			});

			if (response.ok) {
				const { count } = await response.json();
				totalCount = count; // Update total count
			} else {
				console.error('Failed to fetch total count');
			}
		} catch (error) {
			console.error('Error fetching total count:', error);
		}
	}

	onMount(async () => {
		await fetchTotalCount();
		await fetchProperties();
	});

	async function loadPage(page) {
		currentPage = page; // Update current page
		await fetchProperties(); // Fetch properties for the new page
	}
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

{#if loading}
	<!-- Loader -->
	<div class="flex justify-center items-center min-h-screen">
		<div class="animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-[var(--color-bg-2)] border-t-[var(--color-accent)]"></div>
	</div>
{:else if totalCount === 0}
	<!-- No Properties Message -->
	<div class="flex flex-col items-center justify-center h-screen text-center">
		<h1 class="text-2xl font-semibold text-[var(--color-text)] mb-4">No Properties Found</h1>
		<p class="text-[var(--color-text-muted)] mb-4">
			It seems there are no property information available at the moment. Please check back later!
		</p>
	</div>
{:else}
	<!-- Property Grid -->
	<div class="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-4 p-4">
		{#each properties as property}
			<Card
				link={`/properties/${property.property_id_nma}`}
				address={property.property_id_nma}
				area={property.area}
				additionalInfo={`${property.number_of_sections} units in ${property.number_of_buildings} buildings`}
			/>
		{/each}
	</div>

	<!-- Sticky Pagination -->
	<div class="sticky bottom-0 bg-[var(--color-bg-1)] shadow-md p-4 m-0 rounded-t-lg">
		<Pagination
			{totalCount}
			{itemsPerPage}
			bind:currentPage
			onPageChange={loadPage}
		/>
	</div>
{/if}

<style lang="postcss">
	:global(html) {
		background-color: theme(colors.gray.100);
		scroll-behavior: smooth;
	}
</style>
