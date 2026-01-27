<script>
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { user } from '../../../stores/auth.js';
    import Modal from '../../../components/Modal.svelte';

    const id = $page.params.id;

    let adDetails = null;
    let loading = true;

    let hasWriteAccess = false;
    let userDetails;
    let showModal = false; // To control modal visibility
    $: userDetails = $user; // Reactive store subscription

    async function fetchAdDetails(id) {
        try {
            const response = await fetch(`http://localhost:8000/api/v1/ads/${id}`);
            if (response.ok) {
                adDetails = await response.json();
                checkWriteAccess(adDetails.property_id_nma);
            } else {
                console.log('Failed to fetch ad details');
            }
        } catch (err) {
            console.log('Error fetching ad details');
        } finally {
            loading = false;
        }
    }

    async function checkWriteAccess(propertyId) {
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
            }
        } catch (error) {
            console.error('Error checking write access:', error);
        }
    }

    async function deleteAd() {
        try {
            const response = await fetch(`http://localhost:8000/api/v1/ads/${id}?property_id_nma=${adDetails.property_id_nma}`, {
                method: 'DELETE',
                headers: {
                    Authorization: `${userDetails.token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                // alert('Listing deleted successfully!');
                window.location.href = '/listings/me';
            } else {
                alert('Failed to delete the listing.');
            }
        } catch (error) {
            console.error('Error deleting the listing:', error);
        } finally {
            showModal = false; // Close the modal
        }
    }

    function openDeleteModal() {
        showModal = true;
    }

    function closeDeleteModal() {
        showModal = false;
    }

    onMount(() => {
        fetchAdDetails(id);
    });
</script>

{#if loading}
	<div class="flex justify-center items-center min-h-screen">
		<div class="animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-[var(--color-bg-2)] border-t-[var(--color-accent)]"></div>
	</div>
{:else if adDetails}
    <!-- Property Details -->
    <div class="p-8 space-y-6">
        <!-- Property Image -->
        <div class="relative w-full h-96 rounded-lg overflow-hidden shadow-md">
			<img
				src="/property-placeholder.jpg"
				alt="Property"
				class="w-full h-full object-cover"
			/>
			<div class="absolute flex justify-between bottom-0 left-0 bg-gradient-to-t from-black/90 to-40 w-full p-4 pt-96 text-white">
				<!-- Centered Full Address -->
				<div class="absolute bottom-16 left-1/2 transform -translate-x-1/2 text-center">
					<h1 class="text-2xl font-bold">📍{adDetails.address}</h1>
				</div>
				<!-- Left Details -->
				<div>
					<p class="text-lg text-white">🔗{adDetails.property_id_nma} • NOK {adDetails.price.toLocaleString()}</p>
				</div>
				<!-- Buttons on the right side -->
				{#if hasWriteAccess}
					<div class="flex gap-2">
						<a
							href={`/listings/${adDetails.id}/edit`}
							class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition hover:no-underline"
						>
							Edit Listing
						</a>
						<button
							on:click={openDeleteModal}
							class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition"
						>
							Delete Listing
						</button>
					</div>
				{/if}
			</div>
		</div>

        <!-- Title, Type, Status, Price, and Link -->
        <div class="space-y-4">
            <h1 class="text-3xl font-bold">{adDetails.title}</h1>
            <p class="text-sm text-gray-400">Type: {adDetails.type} | Status: {adDetails.status}</p>
            <p class="text-lg font-semibold">Price: NOK {adDetails.price.toLocaleString()}</p>
            <a 
                href={`/properties/${adDetails.property_id_nma}`} 
                class="text-blue-400 hover:underline"
            >
                View Property Details →
            </a>
        </div>

        <!-- Description -->
        <div class="description mt-4 text-gray-200 text-justify">
            {#each adDetails.description.split('\n') as paragraph}
                <p class="mb-4">{paragraph}</p>
            {/each}
        </div>

        <!-- Listed By -->
        <div class="space-y-2">
            <h2 class="text-lg font-semibold">Posted By</h2>
            <p class="text-gray-400">{adDetails.listed_by}</p>
        </div>
    </div>

    <!-- Modal for delete confirmation -->
    {#if showModal}
        <Modal
            title="Confirm Deletion"
            message="Are you sure you want to delete this listing? This action cannot be undone."
            onConfirm={deleteAd}
            onCancel={closeDeleteModal}
        />
    {/if}
{:else}
    <div class="flex justify-center items-center min-h-screen">
        <p class="text-xl text-[var(--color-text-muted)]">No listing details found</p>
    </div>
{/if}

<style>
    :global(body) {
        background-color: #1a202c; /* Dark gray background for the page */
    }
</style>
