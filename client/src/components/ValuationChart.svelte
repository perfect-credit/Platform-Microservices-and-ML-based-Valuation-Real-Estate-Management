<script>
    import LineChart from './LineChart.svelte';
    import { onMount } from 'svelte';

    export let unitId;

    let data = null;
    let valuationFields = [
        { field: 'rental_valuation', title: 'Rental Valuation Over Time' },
        { field: 'comparables_valuation', title: 'Comparables Valuation Over Time' },
        { field: 'listing_valuation', title: 'Listing Valuation Over Time' },
        { field: 'transaction_valuation', title: 'Transaction Valuation Over Time' }
    ];

    async function fetchValuationData() {
        try {
            const response = await fetch(`http://localhost:8000/api/v1/spm/units/${unitId}/valuations?date=2030-01-01`);
            if (response.ok) {
                data = await response.json();
            } else {
                console.log('Error fetching valuation data');
            }
        } catch (error) {
            console.error(error);
        }
    }

    onMount(async () => {
        await fetchValuationData();
    });
</script>

{#if data}
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        {#each valuationFields as { field, title }}
            <div class="rounded-lg shadow-lg transition hover:shadow-xl hover:scale-105 duration-200">
                <!-- Chart container -->
                <div class="w-full h-80">
                    <LineChart
                        data={data}
                        title={title}
                        field={field}
                    />
                </div>
            </div>
        {/each}
    </div>
{/if}
