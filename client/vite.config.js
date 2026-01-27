import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	optimizeDeps: {
		include: ['svelte-icons/fa'], // Include the specific module
	},
	ssr: {
		noExternal: ['svelte-icons'], // Ensure `svelte-icons` is not excluded during SSR
	}
});
