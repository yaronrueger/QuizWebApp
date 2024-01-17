<script lang="ts">
	import { Button, Card, Span } from 'flowbite-svelte';

	export let userInfo = {
		completedQuizzes: 0,
		allPoints: 0
	};
</script>

<Card class="flex" size="lg">
	<div class="h-full flex flex-col justify-between">
		<div>
			<h5 class="mb-4 text-3xl font-bold tracking-tight text-gray-900 dark:text-white">
				Deine Punkte: 📊
			</h5>
			<span class="my-4 text-lg"
				>Du hast bereits <Span highlight>{userInfo.completedQuizzes}</Span> Quizze absolviert</span
			>
			<p class="my-2 text-lg font-normal text-gray-700 dark:text-gray-400 leading-tight">
				{userInfo.allPoints > 0
					? 'Du hast schon ' + userInfo.allPoints + ' Punkte gesammelt!'
					: 'Du hast noch keine Punkte gesammelt!'}
			</p>
		</div>
		<div class="flex justify-between items-center mt-4">
			<Button class="w-fit" href={`/explore`}>Quizze entdecken</Button>
		</div>
	</div>
</Card>
