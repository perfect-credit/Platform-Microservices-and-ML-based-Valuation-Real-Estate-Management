<script>
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { user } from '../../../../stores/auth.js';
    import ListingForm from '../../../../components/ListingForm.svelte';

    let userDetails;
	$: userDetails = $user; // Reactive store subscription

    async function handleFormSubmit(newListing) {
        try {
            const response = await fetch('http://localhost:8000/api/v1/ads', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `${userDetails.token}` },
                body: JSON.stringify(newListing)
            });

            if (response.ok) {
                const createdAd = await response.json(); // Assuming the response includes the created ad details
                console.log(createdAd);
                let url = `/listings/${createdAd.id}`;
                console.log(url);
                goto(url);
            } else {
                alert('Failed to create listing');
            }
        } catch (error) {
            console.error(error);
        }
    }

    async function checkWriteAccess() {
		try {
			const response = await fetch(`http://localhost:8000/api/v1/ads/has-access?property_id_nma=${propertyId}`, {
				method: 'GET',
				headers: {
					Authorization: `${userDetails.token}`, // Include token in the Authorization header
					'Content-Type': 'application/json',
				},
			});
			if (response.ok) {
				const data = await response.json();
				hasWriteAccess = data.success;
			} else {
				console.error('Failed to check write access');
				return false;
			}
		} catch (error) {
			console.error('Error checking write access:', error);
			return false;
		}
	}

    let hasWriteAccess = false;
    let propertyId = $page.params.property_id_nma;

    onMount(async () => {
        await checkWriteAccess();
    });
</script>

{#if hasWriteAccess}
    <ListingForm onSubmit={handleFormSubmit} listing={{ property_id_nma: $page.params.property_id_nma }} token={userDetails.token} />
{:else}
    <div class="flex justify-center items-center min-h-screen">
        <p class="text-xl text-[var(--color-text-muted)]">You do not have permission to create a listing for this property</p>
    </div>
{/if}
