<script>
	export let gridData = []; // Accept grid data as a prop
</script>

<div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
	{#each gridData as item}
		<div class="flex flex-col items-center justify-center bg-[var(--color-bg-2)] p-4 rounded-md shadow-md transition-transform transform hover:scale-105 hover:shadow-lg">
			<span class="text-2xl font-bold">{item.value}</span>
			<span class="text-sm text-[var(--color-text-muted)]">{item.label}</span>
		</div>
	{/each}
</div>
