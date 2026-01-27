<script>
	import { onMount } from 'svelte';
    import { isAuthenticated, user } from '../../stores/auth.js';

	let phoneNumber = '';
	let otp = '';
	let otpSent = false; // Track whether the OTP is sent
	let errorMessage = '';
	let isLoading = false;

	// Function to send OTP
	async function sendOtp() {
		if (!phoneNumber) {
			errorMessage = 'Please enter a valid phone number.';
			return;
		}
		errorMessage = '';
		isLoading = true;
		try {
			// Replace with your actual API endpoint
			const response = await fetch(`http://localhost:8000/api/v1/auth/otp?phone-number=${phoneNumber}`, {
				method: 'GET',
				headers: { 'Content-Type': 'application/json' },
			});
			if (response.ok) {
				otpSent = true;
			} else {
				const result = await response.json();
				errorMessage = result.message || 'Failed to send OTP.';
			}
		} catch (error) {
			errorMessage = 'Error sending OTP. Please try again.';
		} finally {
			isLoading = false;
		}
	}

	// Function to verify OTP
	async function verifyOtp() {
		if (!otp || otp.length !== 6) {
			errorMessage = 'Please enter a valid 6-digit OTP.';
			return;
		}
		errorMessage = '';
		isLoading = true;
		try {
			// Replace with your actual API endpoint
			const response = await fetch('http://localhost:8000/api/v1/auth/login', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ phone_number: phoneNumber, otp: otp }),
			});
			if (response.ok) {
				const result = await response.json();

				// Update stores with authentication data
				isAuthenticated.set(true);
				user.set({
					token: result.access_token,
					phone_number: phoneNumber, // Store additional user details if needed
				});

				// Update localStorage manually if necessary
				localStorage.setItem('isAuthenticated', 'true');
				localStorage.setItem(
					'user',
					JSON.stringify({ token: result.access_token, phone_number: phoneNumber })
				);

				// Redirect to the dashboard or home page
				window.location.href = '/';
			} else {
				const result = await response.json();
				errorMessage = result.message || 'Invalid OTP. Please try again.';
			}
		} catch (error) {
			errorMessage = 'Error verifying OTP. Please try again.';
		} finally {
			isLoading = false;
		}
	}
</script>

<div class="min-h-screen bg-[var(--color-bg-1)] flex items-center justify-center">
	<div class="bg-[var(--color-bg-2)] p-8 rounded-lg shadow-lg w-full max-w-sm">
		<h1 class="text-xl font-bold text-[var(--color-text)] text-center mb-6">Login</h1>

		<!-- Phone Number Input -->
		{#if !otpSent}
			<div>
				<label for="phone" class="block text-sm text-[var(--color-text)] mb-2">Phone Number</label>
				<input
					type="tel"
					id="phone"
					placeholder="Enter your phone number"
					bind:value={phoneNumber}
					class="w-full px-4 py-2 border rounded-md bg-[var(--color-bg-1)] text-[var(--color-text)] focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)]"
				/>
				{#if errorMessage}
					<p class="text-red-500 text-sm mt-2">{errorMessage}</p>
				{/if}
				<button
					class="w-full mt-4 px-4 py-2 bg-[var(--color-accent)] text-white rounded-md hover:bg-opacity-90 transition"
					on:click={sendOtp}
					disabled={isLoading}>
					{isLoading ? 'Sending...' : 'Send OTP'}
				</button>
			</div>
		{:else}
			<!-- OTP Input -->
			<div>
				<label for="otp" class="block text-sm text-[var(--color-text)] mb-2">OTP</label>
				<input
					type="text"
					id="otp"
					placeholder="Enter OTP"
					bind:value={otp}
					class="w-full px-4 py-2 border rounded-md bg-[var(--color-bg-1)] text-[var(--color-text)] focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)]"
				/>
				{#if errorMessage}
					<p class="text-red-500 text-sm mt-2">{errorMessage}</p>
				{/if}
				<button
					class="w-full mt-4 px-4 py-2 bg-[var(--color-accent)] text-white rounded-md hover:bg-opacity-90 transition"
					on:click={verifyOtp}
					disabled={isLoading}>
					{isLoading ? 'Verifying...' : 'Verify OTP'}
				</button>
			</div>
		{/if}
	</div>
</div>
