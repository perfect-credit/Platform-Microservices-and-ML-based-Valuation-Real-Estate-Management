<script>
	import { page } from '$app/stores';
	import logo from '$lib/images/svelte-logo.svg';
	import { FaExternalLinkAlt } from 'svelte-icons/fa';
	import NavButton from '../components/NavButton.svelte';
	import { isAuthenticated, user } from '../stores/auth.js';

	let loggedIn = false;
	isAuthenticated.subscribe(value => {
		loggedIn = value;
	});

	let userDetails = null;
	user.subscribe(value => {
		userDetails = value;
	});

	function logout() {
		isAuthenticated.set(false);
		user.set(null);
		window.location.href = '/login';
	}
</script>

<header class="bg-[var(--color-bg-1)] text-[var(--color-text)] flex justify-between items-center px-6 py-4 border-b border-[var(--color-border)] fixed top-0 left-0 right-0 z-50">
	<!-- Left Logo with Search Bar -->
	<div class="flex items-center space-x-4">
		<a href="/" class="flex items-center">
			<img src="/logo.png" alt="Smart Haven" class="w-25 h-10" />
		</a>
		<div class="ml-6">
			<input
				type="text"
				placeholder="Search properties..."
				class="bg-[var(--color-bg-2)] text-[var(--color-text)] rounded-lg px-4 py-2 border border-[var(--color-border)] focus:border-[var(--color-accent)] focus:outline-none w-96"
			/>
		</div>
	</div>

	{#if loggedIn}
		<!-- Center Buttons -->
		<nav>
			<ul class="flex space-x-8">
				<NavButton label="Properties" link="/" />
				<NavButton label="Listings" link="/listings" />
				<NavButton label="API Sale" link="http://127.0.0.1:8000/docs" target="_blank" icon={FaExternalLinkAlt} />
			</ul>
		</nav>

		<!-- Right Buttons for User -->
		<div class="flex space-x-4">
			<ul class="flex space-x-4">
				<NavButton label="My Properties" link="/properties/me" />
				<NavButton label="My Listings" link="/listings/me" />
				<button on:click={logout} class="px-4 py-2 text-lg bg-red-500 text-white rounded-lg">Logout</button>
			</ul>
		</div>
	{/if}
</header>
