import { redirect } from '@sveltejs/kit';

export function load() {
    // Redirect to the index page or another page
    throw redirect(302, '/'); // Temporary redirect
}
