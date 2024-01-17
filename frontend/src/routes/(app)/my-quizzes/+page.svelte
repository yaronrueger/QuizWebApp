<script lang="ts">
	import { Heading } from 'flowbite-svelte';
	import type { quizInfo } from '../../../config/navigation';
	import QuizInfoCard from '../../../components/User/quizInfoCard.svelte';
	import { API_BASE_PATH } from '@config/api';
	import { accessToken } from '@config/stores';
	import { get } from 'svelte/store';
	import axios from 'axios';
	import { onMount } from 'svelte';
	let data: quizInfo[] = [];

	async function loadData() {
		await axios
			.get(`${API_BASE_PATH}/user/quizzes`, {
				headers: { Authorization: `Bearer ${get(accessToken)}` }
			})
			.then((response) => {
				data = response.data.Quizes;
			});
	}

	onMount(async () => {
		await loadData();
	});
</script>

<Heading class="p-8" tag="h1" customSize="text-3xl">Meine Quizze</Heading>
<div class="grid grid-cols-3 gap-8 mt-2 mx-10 justify-center">
	{#each data as quiz}
		<QuizInfoCard {quiz} />
	{/each}
</div>
