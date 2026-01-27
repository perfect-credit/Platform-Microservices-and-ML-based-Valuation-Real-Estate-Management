<script>
	export let link = '#'; // Link to the property details page
	export let address = ''; // Property address
	export let area = ''; // Property area
	export let price = ''; // Property price
	export let additionalInfo = ''; // Optional additional information
</script>

<a href={link} class="card block bg-[var(--color-bg-2)] text-[var(--color-text)] shadow-lg rounded-lg overflow-hidden transition hover:shadow-xl hover:scale-105 duration-200 no-underline hover:no-underline">
	<!-- Property Image -->
	<div class="card-image">
		<img src="/property-placeholder.jpg" alt="" class="w-full h-48 object-cover" />
	</div>

	<!-- Property Information -->
	<div class="card-content p-4">
		<h2 class="text-lg font-bold">{address}</h2>
		{#if area !== ''}
			<p class="text-sm font-semibold mt-2 text-[var(--color-text-muted)]"><strong>Area:</strong> {area} m²</p>
		{/if}

		{#if price}
			<p class="text-sm font-semibold mt-2 text-[var(--color-text-muted)]"><strong>Price:</strong> NOK {price.toLocaleString()}</p>
		{/if}

		{#if additionalInfo}
			<p class="text-sm text-[var(--color-text)] mt-2">{additionalInfo}</p>
		{/if}
	</div>
</a>


<style>
	.card {
		width: 100%;
		max-width: 400px;
	}
</style>
