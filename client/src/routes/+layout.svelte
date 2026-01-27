<script>
	import Header from './Header.svelte';
	import '../app.css';
	import { page } from '$app/stores';
	import { isAuthenticated, user } from '../stores/auth.js';

	let authenticated;
	let userDetails;

	// Use Svelte's `$` syntax for reactivity
	$: authenticated = $isAuthenticated;
	$: userDetails = $user;

	const isLoginPage = $page.url.pathname === '/login';
</script>

<div class="app">
	{#if authenticated || isLoginPage}
		{#if !isLoginPage}
			<Header />
		{/if}
		<main>
			<slot />
		</main>
	{/if}

	{#if !authenticated && !isLoginPage}
		<script>
			window.location.href = '/login';
		</script>
	{/if}
</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}

	main {
		flex: 1;
		display: flex;
		flex-direction: column;
		padding: 0;
		width: 100%;
		max-width: 75%;
		margin: 5rem auto 0 auto;
		box-sizing: border-box;
	}
</style>
