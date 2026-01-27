<script>
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { user } from '../../../../stores/auth.js';
    import ListingForm from '../../../../components/ListingForm.svelte';

    let userDetails;
	$: userDetails = $user; // Reactive store subscription

    const id = $page.params.id;
    let propertyId = null;
    $: console.log(propertyId);

    let adDetails = null;
    let loading = true;

    // Fetch the ad details from the backend using the ID from the route
    async function fetchAdDetails(id) {
        try {
            const response = await fetch(`http://localhost:8000/api/v1/ads/${id}`);
            if (response.ok) {
                // only keep title, description, price, address, type, and status from the response into adDetails
                let data = await response.json();
                console.log(data);
                adDetails = {
                    title: data.title,
                    description: data.description,
                    price: data.price,
                    address: data.address,
                    type: data.type,
                    status: data.status
                };
                propertyId = data.property_id_nma;
                console.log(adDetails);
            } else {
                console.log('Failed to fetch ad details');
            }
        } catch (err) {
            console.log('Error fetching ad details');
        } finally {
            loading = false;
        }
    }

    async function handleFormSubmit(newListing) {
        try {
            const response = await fetch(`http://localhost:8000/api/v1/ads/${id}?property_id_nma=${propertyId}`, {
                method: 'PATCH',
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

    onMount(async () => {
        await fetchAdDetails(id);
        await checkWriteAccess();
    });
</script>

{#if loading}
    <div class="flex justify-center items-center min-h-screen">
        <div class="animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-[var(--color-bg-2)] border-t-[var(--color-accent)]"></div>
    </div>
{:else if hasWriteAccess}
    <ListingForm onSubmit={handleFormSubmit} listing={adDetails} isUpdate={true} token={userDetails.token} propertyId={propertyId} />
{:else}
    <div class="flex justify-center items-center min-h-screen">
        <p class="text-xl text-[var(--color-text-muted)]">You do not have permission to create a listing for this property</p>
    </div>
{/if}
