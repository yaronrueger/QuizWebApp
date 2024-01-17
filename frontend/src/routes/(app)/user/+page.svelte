<script lang="ts">
	import axios from 'axios';
	import { Heading, P } from 'flowbite-svelte';
	import type { quizInfo } from '../../../config/navigation';
	import QuizInfoCard from '../../../components/User/quizInfoCard.svelte';
	import { accessToken } from '@config/stores';
	import { onMount } from 'svelte';
	import { get } from 'svelte/store';
	import { API_BASE_PATH } from '@config/api';

	let userinfo = {} as { id: number; username: string };
	let quizzes: quizInfo[] = [];

	onMount(() => {
		loadData();
	});

	async function loadData() {
		const token = get(accessToken);
		const config = {
			headers: { Authorization: `Bearer ${token}` }
		};

		axios
			.get(`${API_BASE_PATH}/user/me`, config)
			.then((response) => {
				userinfo = {
					id: response.data.id,
					username: response.data.username
				};
			})
			.catch((error) => {
				console.log(error);
			});

		axios.get(`${API_BASE_PATH}/user/quizzes`, config).then((response) => {
			quizzes = response.data.Quizes;
		});
	}
</script>

<Heading class="p-8" tag="h1" customSize="text-3xl">Deine Nutzer Informationen</Heading>
{#if userinfo.id != undefined}
	<h5 class="mb-1 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
		Dein Username: {userinfo.username}
	</h5>
	<h5 class="mb-1 text-lg font-bold tracking-tight text-gray-900 dark:text-white">
		Deine ID: {userinfo.id}
	</h5>
{/if}
<h5 class="mt-8 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">Deine Quizes:</h5>
<div class="grid grid-cols-3 gap-4 mt-2 justify-center">
	{#each quizzes as quiz}
		<QuizInfoCard {quiz} />
	{/each}
</div>
