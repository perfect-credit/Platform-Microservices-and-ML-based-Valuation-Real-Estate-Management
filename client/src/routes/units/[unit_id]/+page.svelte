<script>
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import NumberGrid from '../../../components/NumberGrid.svelte';
    import Card from '../../../components/Card.svelte';
    import Pagination from '../../../components/Pagination.svelte';
	import ValuationChart from '../../../components/ValuationChart.svelte';

    let unitId = $page.params.unit_id;
    let loading = true;

    let unitDetails = null;
    let propertyDetails = null;
    let similarUnits = null;

    let gridData = [];

    let currentAdPage = 1;
    const adsPerPage = 20;
    let adCount = null;
    let paginatedAds = [];

    async function fetchUnitDetails() {
        try {
            const response = await fetch(`http://localhost:8000/api/v1/spm/units/${unitId}`);
            if (response.ok) {
                unitDetails = await response.json();
                loading = false;

                fetchPropertyDetails();
                updateGridData();
                fetchAdCounts();
                fetchAds();
                fetchSimilarUnits();
            } else {
                console.log('Error fetching unit details');
            }
        } catch (error) {
            console.error(error);
        }
    }

    async function fetchPropertyDetails() {
        try {
            const response = await fetch(`http://localhost:8000/api/v1/spm/properties/${unitDetails.property_id_nma}`);
            if (response.ok) {
                propertyDetails = await response.json();
                loading = false;
            } else {
                console.log('Error fetching property details');
            }
        } catch (error) {
            console.error(error);
        }
    }

    async function fetchSimilarUnits() {
        try {
            const response = await fetch(`http://localhost:8000/api/v1/spm/properties/${unitDetails.property_id_nma_main}`);
            if (response.ok) {
                let data = await response.json();
                // take units that have a different property_id_nma from the current unit from data.units array
                similarUnits = data.units.filter(unit => unit.property_id_nma !== unitDetails.property_id_nma).slice(0, 4);
                console.log(`Similar Units before: ${similarUnits.length}`);
                // if length of similarUnits is less than 4, add the remaining from data.units array
                if (similarUnits.length < 4) {
                    similarUnits.push(...data.units.slice(0, 4 - similarUnits.length));
                }
                console.log(`Similar Units after: ${similarUnits.length}`);
            } else {
                console.log('Error fetching property details');
            }
        } catch (error) {
            console.error(error);
        }
    }

    async function fetchAds() {
        try {
            const response = await fetch(`http://localhost:8000/api/v1/ads?property_id_nma=${unitDetails.property_id_nma}&page=${currentAdPage}`);
            if (response.ok) {
                const data = await response.json();
                paginatedAds = data;
            } else {
                console.log('Error fetching ads');
            }
        } catch (error) {
            console.error(error);
        }
    }

    async function fetchAdCounts() {
        try {
            const response = await fetch(`http://localhost:8000/api/v1/ads/count?property_id_nma=${unitDetails.property_id_nma}`);
            if (response.ok) {
                const data = await response.json();
                adCount = data.count;
            } else {
                console.log('Error fetching ad count');
            }
        } catch (error) {
            console.error(error);
        }
    }

    // Function to prepare data for the numbers grid
	function updateGridData() {
		if (!unitDetails) return;

        let rawGridData = [];
        rawGridData.push({ value: `${unitDetails.floor_number}`, label: 'On Floor' });
        rawGridData.push({ value: `${unitDetails.land_area} m²`, label: 'Property Land Area' });
        rawGridData.push({ value: `${unitDetails.bra} m²`, label: 'Built Residential Area' });
        rawGridData.push({ value: `${unitDetails.rooms}`, label: 'Number of Rooms' });
        rawGridData.push({ value: `${unitDetails.bedrooms}`, label: 'Number of Bedrooms' });
        rawGridData.push({ value: `${unitDetails.bathrooms}`, label: 'Number of Bathrooms' });
        rawGridData.push({ value: `${unitDetails.wcs}`, label: 'Number of WCs' });
        rawGridData.push({ value: unitDetails.in_beach_zone ? 'Yes': 'No', label: 'In Beach Zone' });
        rawGridData.push({ value: `${unitDetails.nearest_train_station_distance} km`, label: 'Nearest Train Station' });
        rawGridData.push({ value: `${unitDetails.nearest_bus_station_distance} km`, label: 'Nearest Bus Station' });
        rawGridData.push({ value: `${unitDetails.nearest_ferry_terminal_distance} km`, label: 'Nearest Ferry Terminal' });
        rawGridData.push({ value: `${unitDetails.nearest_tram_station_distance} km`, label: 'Nearest Tram Station' });
        rawGridData.push({ value: `${unitDetails.nearest_underground_station_distance} km`, label: 'Nearest Underground Station' });
        rawGridData.push({ value: `${unitDetails.nearest_gondola_lift_station_distance} km`, label: 'Nearest Gandola Lift Station' });
        rawGridData.push({ value: `${unitDetails.nearest_airport_distance} km`, label: 'Nearest Airport' });
        rawGridData.push({ value: `${unitDetails.nearest_kindergartens_distance} km`, label: 'Nearest Kindergarten' });
        rawGridData.push({ value: `${unitDetails.nearest_elementary_middle_school_distance} km`, label: 'Nearest Middle School' });
        rawGridData.push({ value: `${unitDetails.nearest_high_school_distance} km`, label: 'Nearest High School' });
        rawGridData.push({ value: `${unitDetails.nearest_fire_station_distance} km`, label: 'Nearest Fire Station' });

        // Filter out items where the value is null or undefined
        gridData = rawGridData.filter(item => item.value !== null && item.value !== undefined);
	}

    onMount(() => {
        fetchUnitDetails();
    });

    function handleAdsPageChange(page) {
        currentAdPage = page;
        fetchAds();
    }
</script>

{#if loading}
	<div class="flex justify-center items-center min-h-screen">
		<div class="animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-[var(--color-bg-2)] border-t-[var(--color-accent)]"></div>
	</div>
{:else if unitDetails}
    <!-- Unit Details -->
	<div class="p-8 space-y-6">
		<!-- Property Image -->
		<div class="relative w-full h-96 rounded-lg overflow-hidden shadow-md">
			<img
				src="/property-placeholder.jpg"
				alt="Property"
				class="w-full h-full object-cover"
			/>
			<div class="absolute bottom-0 left-0 bg-gradient-to-t from-black/90 to-40 w-full p-4 pt-96 text-white">
				<h1 class="text-2xl font-bold">📍{unitDetails.full_address}</h1>
				<p class="text-lg">🔗{unitDetails.property_id_nma} • {unitDetails.bra} m²</p>
			</div>
		</div>

		<!-- Grid for Numbers -->
		<NumberGrid {gridData} />

        <h2 class="text-xl font-semibold mb-4">Valuations</h2>
        <ValuationChart unitId={unitId} />

        <!-- Listings Section -->
        {#if paginatedAds.length > 0}
            <h2 class="text-xl font-semibold mb-4">Listings</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                {#each paginatedAds as ad}
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
{/if}
