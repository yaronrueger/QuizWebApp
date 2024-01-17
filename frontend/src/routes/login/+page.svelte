<script lang="ts">
	import { Card, Button, Label, Input, Checkbox } from 'flowbite-svelte';
	import '../../app.postcss';
	import { onMount } from 'svelte';
	import { accessToken } from '../../config/stores';
	import axios from 'axios';
	import { API_BASE_PATH } from '@config/api';

	onMount(() => {
		accessToken.set(undefined);
	});

	async function onSubmit(event: Event) {
		event.preventDefault();
		const form = event.currentTarget as HTMLFormElement;
		const formData = new FormData(form);
		const username = formData.get('username');
		const password = formData.get('password');
		let success = false;
		try {
			const response = await axios({
				method: 'post',
				headers: { 'content-type': 'application/x-www-form-urlencoded' },
				url: `${API_BASE_PATH}/login`,
				data: {
					username: username,
					password: password
				}
			});
			success = true;
			accessToken.set(response.data.access_token);
		} catch (error) {
			console.log('🚀 ~ file: +page.server.ts:55 ~ login: ~ error:', error);
		}

		if (success) {
			window.location.assign('/');
		}
	}
</script>

<div class="w-full flex h-screen justify-center items-center">
	<Card class="w-full max-w-md">
		<form class="flex flex-col space-y-6" on:submit={onSubmit}>
			<h3 class="text-xl font-medium text-gray-900 dark:text-white">Anmelden</h3>
			<Label class="space-y-2">
				<span>Username</span>
				<Input name="username" placeholder="coolerUser1" required />
			</Label>
			<Label class="space-y-2">
				<span>Dein Passwort</span>
				<Input type="password" name="password" placeholder="•••••" required />
			</Label>
			<div class="flex items-start">
				<Checkbox>Angemeldet bleiben</Checkbox>
				<a href="/" class="ml-auto text-sm text-primary-700 hover:underline dark:text-primary-500">
					Passwort vergessen?
				</a>
			</div>
			<Button formaction="?/login" type="submit" class="w-full">Anmelden</Button>
			<div class="text-sm font-medium text-gray-500 dark:text-gray-300">
				Noch kein Account? <a
					href="/register"
					class="text-primary-700 hover:underline dark:text-primary-500"
				>
					Account erstellen
				</a>
			</div>
		</form>
	</Card>
</div>
