<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { user } from '../../../stores/auth.js';
	import Accordion from '../../../components/Accordion.svelte';
	import Card from '../../../components/Card.svelte';
	import Pagination from '../../../components/Pagination.svelte';
	import NumberGrid from '../../../components/NumberGrid.svelte';

	let propertyDetails = null;
    let propertyAds = null;
	let similarUnits = null;
	let propertyId = $page.params.property_id_nma; // Fetch the dynamic ID from the route
	let loading = true;

	// Pagination variables for units
	let currentPage = 1;
	const itemsPerPage = 4; // Number of units per page
	let paginatedUnits = [];

	// Pagination variables for owners
	let ownerPage = 1;
	const ownersPerPage = 8; // Number of owners per page
	let paginatedOwners = [];

    let currentAdPage = 1;
    const adsPerPage = 20;
    let adCount = null;

	// Number grid data
	let gridData = [];

	let hasWriteAccess = false;
	let userDetails;
	$: userDetails = $user; // Reactive store subscription

    async function fetchPropertyAds() {
        try {
            const response = await fetch(`http://localhost:8000/api/v1/ads?property_id_nma=${propertyId}&page=${currentAdPage}`);
            if (response.ok) {
                const ads = await response.json();
                if (ads.length > 0) {
                    propertyAds = ads;
                }
            } else {
                console.error('Failed to fetch property ads');
            }
        } catch (error) {
            console.error('Error fetching property ads:', error);
        }
    }

    async function fetchAdCounts() {
        try {
            const response = await fetch(`http://localhost:8000/api/v1/ads/count?property_id_nma=${propertyId}`);
            if (response.ok) {
                const adCounts = await response.json();
                adCount = adCounts.count;
            } else {
                console.error('Failed to fetch ad counts');
            }
        } catch (error) {
            console.error('Error fetching ad counts:', error);
        }
    }

	async function checkWriteAccess() {
		try {
			const response = await fetch(`http://localhost:8000/api/v1/ads/has-access?property_id_nma=${propertyId}`, {
				method: 'GET',
				headers: {
					Authorization: `${userDetails.token}`, // Include token in the Authorization header
					'Content-Type': 'application/json',
				},
			});
			if (response.ok) {
				const data = await response.json();
				hasWriteAccess = data.success;
			} else {
				console.error('Failed to check write access');
				return false;
			}
		} catch (error) {
			console.error('Error checking write access:', error);
			return false;
		}
	}

	// Fetch property details from the backend using the propertyId
	async function fetchPropertyDetails() {
		try {
			const response = await fetch(`http://localhost:8000/api/v1/spm/properties/${propertyId}`);
			if (response.ok) {
				propertyDetails = await response.json();
				updatePaginatedUnits(); // Update paginated units after fetching data
				updateGridData(); // Update the grid data
				updatePaginatedOwners(); // Update paginated owners after fetching data
				checkWriteAccess();

                // Fetch property ads
                fetchPropertyAds();
                fetchAdCounts();

				similarUnits = propertyDetails.units.filter(unit => unit.property_id_nma !== propertyId).slice(0, 4);
				if (similarUnits.length < 4) {
                    similarUnits.push(...propertyDetails.units.slice(0, 4 - similarUnits.length));
                }
			} else {
				console.error('Failed to fetch property details');
			}
		} catch (error) {
			console.error('Error fetching property details:', error);
		} finally {
			loading = false;
		}
	}

	// Function to prepare data for the numbers grid
	function updateGridData() {
		if (!propertyDetails) return;

        let rawGridData = [
            { value: propertyDetails.number_of_buildings, label: 'Buildings' },
            { value: propertyDetails.number_of_sections, label: 'Sections' },
            { value: propertyDetails.area ? `${propertyDetails.area} m²` : null, label: 'Total Area' },
            { value: propertyDetails.number_of_leases, label: 'Leases' },
            { value: propertyDetails.number_of_owners, label: 'Owners' },
            { value: propertyDetails.parking_garage !== null ? (propertyDetails.parking_garage ? 'Yes' : 'No') : null, label: 'Parking Garage' },
        ];

        if (propertyDetails.units.length > 0) {
            rawGridData.push({ value: propertyDetails.units.length, label: 'Units' });
            rawGridData.push({ value: propertyDetails.units[0].in_beach_zone ? 'Yes': 'No', label: 'In Beach Zone' });
            rawGridData.push({ value: `${propertyDetails.units[0].nearest_train_station_distance} km`, label: 'Nearest Train Station' });
            rawGridData.push({ value: `${propertyDetails.units[0].nearest_bus_station_distance} km`, label: 'Nearest Bus Station' });
            rawGridData.push({ value: `${propertyDetails.units[0].nearest_ferry_terminal_distance} km`, label: 'Nearest Ferry Terminal' });
            rawGridData.push({ value: `${propertyDetails.units[0].nearest_tram_station_distance} km`, label: 'Nearest Tram Station' });
            rawGridData.push({ value: `${propertyDetails.units[0].nearest_underground_station_distance} km`, label: 'Nearest Underground Station' });
            rawGridData.push({ value: `${propertyDetails.units[0].nearest_gondola_lift_station_distance} km`, label: 'Nearest Gandola Lift Station' });
            rawGridData.push({ value: `${propertyDetails.units[0].nearest_airport_distance} km`, label: 'Nearest Airport' });
            rawGridData.push({ value: `${propertyDetails.units[0].nearest_kindergartens_distance} km`, label: 'Nearest Kindergarten' });
            rawGridData.push({ value: `${propertyDetails.units[0].nearest_elementary_middle_school_distance} km`, label: 'Nearest Middle School' });
            rawGridData.push({ value: `${propertyDetails.units[0].nearest_high_school_distance} km`, label: 'Nearest High School' });
            rawGridData.push({ value: `${propertyDetails.units[0].nearest_fire_station_distance} km`, label: 'Nearest Fire Station' });
        }

        // Filter out items where the value is null or undefined
        gridData = rawGridData.filter(item => item.value !== null && item.value !== undefined);
	}

	// Function to update paginated units based on the current page
	function updatePaginatedUnits() {
		if (!propertyDetails?.units) return;
		const start = (currentPage - 1) * itemsPerPage;
		const end = start + itemsPerPage;
		paginatedUnits = propertyDetails.units.slice(start, end);
	}

	// Function to update paginated owners based on the current owner page
	function updatePaginatedOwners() {
		if (!propertyDetails?.owners) return;
		const start = (ownerPage - 1) * ownersPerPage;
		const end = start + ownersPerPage;
		paginatedOwners = propertyDetails.owners.slice(start, end);
	}

	// Handle page change for units
	function handlePageChange(page) {
		currentPage = page;
		updatePaginatedUnits();
	}

    function handleAdsPageChange(page) {
        if (page > adCount / adsPerPage) return;
        currentAdPage = page;
        fetchPropertyAds();
    }

	// Handle page change for owners
	function handleOwnerPageChange(page) {
		ownerPage = page;
		updatePaginatedOwners();
	}

	onMount(fetchPropertyDetails);

    function titleCase(s) {
        return s.toLowerCase()
                .split(' ')
                .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                .join(' ');
    }
</script>

{#if loading}
	<div class="flex justify-center items-center min-h-screen">
		<div class="animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-[var(--color-bg-2)] border-t-[var(--color-accent)]"></div>
	</div>
{:else if propertyDetails}
	<!-- Property Details -->
	<div class="p-8 space-y-6">
		<!-- Property Image -->
		<div class="relative w-full h-96 rounded-lg overflow-hidden shadow-md">
			<img
				src="/property-placeholder.jpg"
				alt="Property"
				class="w-full h-full object-cover"
			/>
			<div class="absolute flex justify-between bottom-0 left-0 bg-gradient-to-t from-black/90 to-40 w-full p-4 pt-96 text-white">
				<!-- Centered Full Address -->
				<div class="absolute bottom-16 left-1/2 transform -translate-x-1/2 text-center">
					<h1 class="text-2xl font-bold">📍{propertyDetails.units[0].full_address}</h1>
				</div>
				<!-- Left Details -->
				<div>
					<p class="text-lg text-white">🔗{propertyDetails.property_id_nma} • {propertyDetails.area} m²</p>
				</div>
				<!-- Button on the right side -->
				{#if hasWriteAccess}
					<a
						href={`/properties/${propertyDetails.property_id_nma}/ads`}
						class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition hover:no-underline"
					>
						Create New Listing
					</a>
				{/if}
			</div>
		</div>

		<!-- Grid for Numbers -->
		<NumberGrid {gridData} />

        <!-- Buildings Section -->
        {#if propertyDetails.buildings.length > 0}
            <div class="space-y-4 mt-6">
                <h2 class="text-xl font-semibold mb-4">Buildings</h2>
                <div class="space-y-4">
                    {#each propertyDetails.buildings as building}
                        <Accordion {building} />
                    {/each}
                </div>
            </div>
        {/if}

		<!-- Units Section -->
		{#if propertyDetails.units.length > 0}
			<h2 class="text-xl font-semibold mb-4">Units</h2>
			<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
				{#each paginatedUnits as unit}
					<Card
						link={`/units/${unit.unit_id}`}
						address={unit.address}
						area={unit.bra}
						price={unit.index_valuation}
						additionalInfo={unit.additional_info}
					/>
				{/each}
			</div>
			<Pagination
				totalCount={propertyDetails.units.length}
				itemsPerPage={itemsPerPage}
				bind:currentPage
				onPageChange={handlePageChange}
			/>
		{/if}

		<!-- Owners Section -->
		{#if propertyDetails.owners.length > 0}
			<h2 class="text-xl font-semibold mb-4">Owners</h2>
			<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-4 gap-4">
				{#each paginatedOwners as owner}
					<div class="bg-[var(--color-bg-2)] p-4 rounded-lg shadow-md transition-transform transform hover:scale-105 hover:shadow-lg">
						<p class="text-md font-semibold mb-2"><strong>Name:</strong> {titleCase(owner.name)}</p>
						<p class="text-sm text-[var(--color-text-muted)]">
							<strong>Phone Number:</strong> {owner.phone_number || 'N/A'}
						</p>
					</div>
				{/each}
			</div>
			<Pagination
				totalCount={propertyDetails.owners.length}
				itemsPerPage={ownersPerPage}
				bind:currentPage={ownerPage}
				onPageChange={handleOwnerPageChange}
			/>
		{/if}

        <!-- Listings Section -->
		{#if propertyAds && propertyAds.length > 0}
			<h2 class="text-xl font-semibold mb-4">Listings</h2>
			<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
				{#each propertyAds as ad}
					<Card
						link={`/listings/${ad.id}`}
						address={ad.address}
						price={ad.price}
						additionalInfo={`Located at ${ad.address} is up for ${ad.type}.`}
					/>
				{/each}
			</div>
			<Pagination
				totalCount={adCount}
				itemsPerPage={adsPerPage}
				bind:currentAdPage
				onPageChange={handleAdsPageChange}
			/>
		{/if}

		{#if similarUnits && similarUnits.length > 0}
			<h2 class="text-xl font-semibold mb-4">Similar Properties</h2>
			<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
				{#each similarUnits as unit}
					<Card
						link={`/units/${unit.unit_id}`}
						address={unit.address}
						area={unit.bra}
					/>
				{/each}
			</div>
		{/if}
	</div>
{:else}
	<div class="flex justify-center items-center min-h-screen">
		<p class="text-xl text-[var(--color-text-muted)]">No property details found</p>
	</div>
{/if}

<style>
	:global(body) {
		background-color: var(--color-bg-1);
	}
</style>
