<script>
    import { page } from '$app/stores';
    import { FaExternalLinkAlt } from 'svelte-icons/fa';
    import { onMount } from 'svelte';

    export let label;
    export let link;
    export let icon;
    export let target = null;
</script>

<li
	class="flex items-center rounded-lg px-4 py-2 text-lg transition-all duration-200 ease-in-out hover:bg-[var(--color-bg-2)] hover:text-[var(--color-accent)]"
	class:bg-[var(--color-bg-2)]={$page.url.pathname === link}
	class:text-[var(--color-accent)]={$page.url.pathname === link}
    class:font-bold={$page.url.pathname === link}
>
	<a href="{link}" class="no-underline hover:no-underline" {target}>
		{label}
	</a>
    {#if icon}
        <span class="w-8 h-4 hover:text-[var(--color-accent)]">
            <svelte:component this={icon} />
        </span>
    {/if}
</li>
