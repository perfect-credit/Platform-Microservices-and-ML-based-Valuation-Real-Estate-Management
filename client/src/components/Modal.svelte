<script>
    export let title = 'Confirm Action';
    export let message = 'Are you sure?';
    export let onConfirm;
    export let onCancel;
</script>

<div class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
    <div class="bg-[var(--color-bg-2)] rounded-lg shadow-lg p-6 w-96">
        <h2 class="text-lg font-semibold mb-4">{title}</h2>
        <p class="text-gray-300 mb-6">{message}</p>
        <div class="flex justify-end gap-4">
            <button
                class="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition"
                on:click={onCancel}
            >
                Cancel
            </button>
            <button
                class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition"
                on:click={onConfirm}
            >
                Confirm
            </button>
        </div>
    </div>
</div>
