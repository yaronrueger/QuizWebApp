<script lang="ts">
	import { A, Heading } from 'flowbite-svelte';
	import Leaderboard from '@component/Home/leaderboard.svelte';
	import axios from 'axios';
	import { API_BASE_PATH } from '@config/api';
	import { page } from '$app/stores';
	import { accessToken } from '@config/stores';
	import type { QuizByID } from '@config/navigation';
	const config = {
		headers: { Authorization: `Bearer ${$accessToken}` }
	};

	let quizData: Promise<QuizByID> = getQuizTitle();

	async function getQuizTitle(): Promise<QuizByID> {
		let data: QuizByID = {
			id: 0,
			creator: 0,
			title: '',
			category: 0,
			created: '',
			desc: '',
			modified: '',
			plays: 0
		};

		await axios
			.get(`${API_BASE_PATH}/quizzes/quiz?quiz_id=${$page.params.quizID}`, config)
			.then((response) => {
				data = response.data;
			})
			.catch((error) => {
				console.log(error);
			});

		return data;
	}
</script>

{#await quizData then quiz}
	<div class="w-full h-full">
		<Heading
			class="p-8 mb-5 w-full flex content-center justify-center"
			tag="h1"
			customSize="text-3xl"
			>Bestenliste🎯: {quiz.title}
		</Heading>

		<div class="h-fit w-full flex content-center justify-center">
			<Leaderboard />
		</div>
	</div>
{/await}
