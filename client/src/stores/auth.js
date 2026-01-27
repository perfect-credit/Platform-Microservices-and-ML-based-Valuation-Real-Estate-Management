import { writable } from 'svelte/store';

export const isAuthenticated = writable(true);
export const user = writable(true);

if (typeof window !== 'undefined') {
	// Initialize from localStorage
	isAuthenticated.set(localStorage.getItem('isAuthenticated') === 'true');
	user.set(JSON.parse(localStorage.getItem('user') || 'null'));

	// Sync store updates back to localStorage
	isAuthenticated.subscribe(value => {
		localStorage.setItem('isAuthenticated', value);
	});
	user.subscribe(value => {
		localStorage.setItem('user', JSON.stringify(value));
	});
}
