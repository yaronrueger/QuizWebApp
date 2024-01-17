<script lang="ts">
	import { Button, Card, Span } from 'flowbite-svelte';

	export let userQuizFacts = {
		createdQuizzes: 0,
		quizUser: 0
	};
</script>

<Card class="flex" size="lg">
	<div class="h-full flex flex-col justify-between">
		<div>
			<h5 class="mb-6 text-3xl font-bold tracking-tight text-gray-900 dark:text-white">
				Deine Quizze: 🧠
			</h5>
			<span class="my-4 text-lg"
				>Du hast bereits <Span highlight>{userQuizFacts.createdQuizzes}</Span> Quizze erstellt.</span
			>
			<p class="my-2 text-lg font-normal text-gray-700 dark:text-gray-400 leading-tight">
				{userQuizFacts.quizUser > 0
					? userQuizFacts.quizUser + ' Nutzer haben bereits dein Quiz gespielt.'
					: 'Bisher haben noch keine User dein Quiz gespielt.'}
			</p>
		</div>
		<div class="flex justify-between items-center mt-10">
			<Button class="w-fit" href={`/my-quizzes`}>Meine Quizze</Button>
		</div>
	</div>
</Card>
