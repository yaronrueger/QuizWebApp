<script lang="ts">
	import { Card, Label, Button, Input, Alert } from 'flowbite-svelte';
	import '../../app.postcss';
	import axios from 'axios';
	import { API_BASE_PATH } from '@config/api';
	import { Icon } from 'svelte-boxicons';

	// TODO

	let showError: boolean = false;

	async function onSubmit(event: Event) {
		const form = event.currentTarget as HTMLFormElement;
		const formData = new FormData(form);
		const username = formData.get('username');
		const password = formData.get('password');
		const passwordConfirm = formData.get('passwordConfirm');
		let success = false;

		if (password !== passwordConfirm) {
			console.log('passwords do not match');
			showError = true;
			return;
		}

		console.log({
			username: username,
			password_hash: password
		});

		try {
			await axios({
				method: 'post',
				headers: { 'content-type': 'application/json' },
				url: `${API_BASE_PATH}/register`,
				data: {
					username: username,
					password_hash: password
				}
			});
			success = true;
		} catch (e) {
			showError = true;
			return;
		}

		// outside of try catch because it doesn't work inside
		if (success) {
			window.location.assign('/login');
		}
	}
</script>

<div class="w-full flex h-screen justify-center items-center">
	<Card class="w-full max-w-md">
		{#if showError}
			<Alert color="red" dismissable>
				<div class="flex flex-row">
					<Icon name="bx-x-regular" class="w-5 h-5 mr-3" />
					Something went wrong!
				</div>
			</Alert>
		{/if}
		<form class="flex flex-col space-y-6" on:submit={onSubmit}>
			<h3 class="text-xl font-medium text-gray-900 dark:text-white">Account erstellen</h3>
			<Label class="space-y-2">
				<span>Username</span>
				<Input name="username" placeholder="coolerUser1" required />
			</Label>
			<Label class="space-y-1">
				<span>Dein Passwort</span>
				<Input type="password" name="password" placeholder="•••••" required />
			</Label>
			<Label class="space-y-1">
				<span>Passwort bestätigen</span>
				<Input type="password" name="passwordConfirm" placeholder="•••••" required />
			</Label>

			<Button formaction="?/register" type="submit" class="w-full">Registrieren</Button>
			<div class="text-sm font-medium text-gray-500 dark:text-gray-300">
				Bereits Account erstellt? <a
					href="/login"
					class="text-primary-700 hover:underline dark:text-primary-500"
				>
					Anmelden
				</a>
			</div>
		</form>
	</Card>
</div>
