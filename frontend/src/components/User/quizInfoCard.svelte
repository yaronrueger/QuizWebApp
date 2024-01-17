<script lang="ts">
	import { Button, Card, Modal, Span } from 'flowbite-svelte';
	import type { quizInfo } from '../../config/navigation';
	import { categoryMap } from '../../config/navigation';
	import { Icon } from 'svelte-boxicons';
	import axios from 'axios';
	import { API_BASE_PATH } from '@config/api';
	import { accessToken } from '@config/stores';

	export let quiz: quizInfo;

	let openModal = false;

	const config = {
		headers: { Authorization: `Bearer ${$accessToken}` }
	};

	function getKeyByValue(value: number) {
		for (const key in categoryMap) {
			if (categoryMap[key] === value) {
				return key;
			}
		}
		return null; // If the value is not found
	}

	async function deleteQuiz() {
		await axios
			.post(`${API_BASE_PATH}/delete/user/quiz?quiz_id=${quiz.id}`, null, config)
			.then((response) => {
				console.log(response);
			})
			.catch((error) => {
				console.log(error);
			});

		openModal = false;
		window.location.reload();
	}
</script>

<Card class="w-full flex" size="lg">
	<div class="h-full flex flex-col justify-between">
		<div>
			<div class="flex flex-row justify-between items-center">
				<h5 class="mb-1 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
					{quiz.title}
				</h5>
				<Icon
					on:click={() => (openModal = true)}
					name="bx-trash-regular"
					class="w-5 h-5 cursor-pointer"
				/>
			</div>
			<p class="mb-3 font-normal text-gray-700 dark:text-gray-400 leading-tight">
				{quiz.desc}
			</p>
		</div>
		<div>
			<p class="mb-3 font-normal text-gray-700 dark:text-gray-400 leading-tight">
				Kategorie: {getKeyByValue(quiz.category)}
			</p>
		</div>
		<div>
			<p class="mb-3 font-normal text-gray-700 dark:text-gray-400 leading-tight">
				Erstellt: {quiz.created}
			</p>
			{#if quiz.modified !== quiz.created}
				<p class="mb-3 font-normal text-gray-700 dark:text-gray-400 leading-tight">
					Modifiziert: {quiz.modified}
				</p>
			{/if}
		</div>
		<div>
			<p class="mb-3 font-normal text-gray-700 dark:text-gray-400 leading-tight">
				<Span highlight>{quiz.plays}</Span> mal wurde deine Quiz bereits gespielt
			</p>
		</div>
	</div>
</Card>

<Modal size="sm" title="Quiz löschen?" bind:open={openModal} autoclose>
	<p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
		Diese Aktion kann nicht rückgängig gemacht werden. Bist du dir wirklich sicher, dass du das Quiz
		löschen möchtest?
	</p>
	<svelte:fragment slot="footer">
		<Button on:click={deleteQuiz}>Quiz löschen</Button>
		<Button color="alternative">Nein</Button>
	</svelte:fragment>
</Modal>
