<script>
    export let building; // Building data passed as a prop
    let open = false; // Accordion open/closed state
</script>

<div class="border border-[var(--color-border)] rounded-lg overflow-hidden">
    <!-- Accordion Header -->
    <div
        class="flex justify-between items-center bg-[var(--color-bg-2)] text-[var(--color-text)] p-4 cursor-pointer"
        on:click={() => (open = !open)}
        type="button"
        aria-hidden="true"
    >
        <h3 class="font-semibold">{building.address || building.building_number}</h3>
        <button class="text-[var(--color-text)] text-xl transform transition-transform duration-300">
            {open ? '▲' : '▼'}
        </button>
    </div>

    <!-- Accordion Content -->
    {#if open}
        <div class="bg-[var(--color-bg-1)] text-[var(--color-text)] p-4 space-y-2">
            <p><span class="font-semibold">Floors:</span> {building.floors}</p>
            <p><span class="font-semibold">Units:</span> {building.units_home}</p>
            <p><span class="font-semibold">Type:</span> {building.building_type_code_name}</p>
            <p><span class="font-semibold">Built Area:</span> {building.built_area || 'N/A'} sqm</p>
            <p><span class="font-semibold">Energy Grade:</span> {building.energy_grade || 'N/A'}</p>
            <p><span class="font-semibold">Elevator:</span> {building.has_elevator ? 'Yes' : 'No'}</p>
            <p><span class="font-semibold">Heating:</span> {building.heating_grade || 'N/A'}</p>
        </div>
    {/if}
</div>
