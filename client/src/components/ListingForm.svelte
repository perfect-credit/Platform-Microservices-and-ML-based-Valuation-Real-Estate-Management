<script>
    export let listing = {
        title: '',
        description: '',
        property_id_nma: '',
        address: '',
        price: '',
        type: '',
    };

    export let onSubmit;
    export let isUpdate = false;
    export let token;
    export let propertyId = null;

    let generatedDescription = null;
    let loadingDescription = false;

    async function getSuggestedDescription() {
        try {
            loadingDescription = true; // Show a loading state for the button
            const id = listing.property_id_nma || propertyId;
            const response = await fetch(`http://localhost:8000/api/v1/ads/description/${id}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `${token}`,
                },
            });
            if (response.ok) {
                let data = await response.json();
                generatedDescription = data.message;

                // Populate the description field with the generated data
                listing.description = generatedDescription;
            } else {
                console.log('Error fetching suggested description');
            }
        } catch (error) {
            console.error('Error:', error);
        } finally {
            loadingDescription = false; // Reset the button state
        }
    }

    function handleSubmit(event) {
        event.preventDefault();
        onSubmit(listing);
    }
</script>

<div class="flex justify-center items-center min-h-screen pb-8 pt-8 bg-gray-800">
    <form on:submit={handleSubmit} class="shadow-md rounded-lg w-full max-w-4xl space-y-6">
        <h1 class="text-2xl font-semibold text-gray-200">
            {isUpdate ? 'Edit Listing' : 'Create New Listing'}
        </h1>

        <!-- Title -->
        <div class="space-y-2">
            <label for="title" class="block text-gray-400">Title</label>
            <input
                id="title"
                type="text"
                bind:value={listing.title}
                class="w-full p-3 rounded-lg bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter title"
                required
            />
        </div>

        <!-- Description -->
        <div class="space-y-2">
            <label for="description" class="block text-gray-400">Description</label>
            <textarea
                id="description"
                bind:value={listing.description}
                class="w-full p-3 rounded-lg bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter description"
                rows="10"
                required
            ></textarea>
            <!-- Generate Button -->
            <div class="flex justify-end mt-2">
                <button
                    type="button"
                    on:click={getSuggestedDescription}
                    class="px-4 py-2 bg-green-500 hover:bg-green-600 rounded-lg text-white font-semibold transition-colors"
                    disabled={loadingDescription}
                >
                    {loadingDescription ? 'Generating...' : 'Generate'}
                </button>
            </div>
        </div>

        <!-- Address -->
        <div class="space-y-2">
            <label for="address" class="block text-gray-400">Address</label>
            <input
                id="address"
                type="text"
                bind:value={listing.address}
                class="w-full p-3 rounded-lg bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter address"
                required
            />
        </div>

        <!-- Price -->
        <div class="space-y-2">
            <label for="price" class="block text-gray-400">Price (NOK)</label>
            <input
                id="price"
                type="number"
                bind:value={listing.price}
                class="w-full p-3 rounded-lg bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter price"
                required
            />
        </div>

        <!-- Type -->
        <div class="space-y-2">
            <label for="type" class="block text-gray-400">Type</label>
            <input
                id="type"
                type="text"
                bind:value={listing.type}
                class="w-full p-3 rounded-lg bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter type"
                required
            />
        </div>

        {#if isUpdate}
        <!-- Status -->
            <div class="space-y-2">
                <label for="status" class="block text-gray-400">Status</label>
                <input
                    id="status"
                    type="text"
                    bind:value={listing.status}
                    class="w-full p-3 rounded-lg bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Enter status"
                    required
                />
            </div>
        {/if}

        <button
            type="submit"
            class="w-full p-3 bg-blue-500 hover:bg-blue-600 rounded-lg text-white font-semibold transition-colors"
        >
            {isUpdate ? 'Update Listing' : 'Create Listing'}
        </button>
    </form>
</div>
