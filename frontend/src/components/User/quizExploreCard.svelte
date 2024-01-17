<script lang="ts">
	import { Badge, Button, Card, Span } from 'flowbite-svelte';
	import type { quizInfo } from '../../config/navigation';
	import { categoryMap } from '../../config/navigation';
	import { Icon } from 'svelte-boxicons';

	export let quiz: quizInfo;

	function getKeyByValue(value: number) {
		for (const key in categoryMap) {
			if (categoryMap[key] === value) {
				return key;
			}
		}
		return null; // If the value is not found
	}
</script>

<Card class="w-full flex" size="xl">
	<div class="h-full flex flex-col justify-between">
		<div>
			<h5 class="mb-3 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
				{quiz.title}
			</h5>
			<div class="mb-3">
				<Badge color="dark" border>
					<Icon name="bx-time-regular" class="w-4 h-4 mr-1" />
					{quiz.created !== quiz.modified
						? new Date(quiz.modified).toLocaleDateString('de')
						: new Date(quiz.created).toLocaleDateString('de')}
				</Badge>
				<Badge color="blue" border>
					<Icon name="bx-user-regular" class="w-4 h-4 mr-1" />
					{quiz.plays}
				</Badge>
				<Badge color="red" border>
					<Icon name="bx-category-regular" class="w-4 h-4 mr-1" />
					{getKeyByValue(quiz.category)}
				</Badge>
				<!-- svelte-ignore empty-block -->
				{#if quiz.points_percentage < 0}
					<Badge color="green" border>
						<Icon name="bx-check-square-regular" class="w-4 h-4 mr-1" />
						-
					</Badge>
				{:else}
					<Badge color="green" border>
						<Icon name="bx-check-square-regular" class="w-4 h-4 mr-1" />
						{Math.trunc(quiz.points_percentage * 100)}%
					</Badge>
				{/if}
			</div>
			<!-- <hr class="my-3" /> -->
			<p class="mb-3 font-normal text-gray-400 dark:text-gray-300 leading-tight">
				{quiz.desc}
			</p>
		</div>
		<hr class="my-3" />
		<div class="flex justify-between">
			<Button href="/ranking/{quiz.id}" color="alternative">
				<Icon name="bx-list-ol-regular" class="w-4 h-4 mr-1" /> Bestenliste
			</Button>
			<Button href="/play/{quiz.id}">
				<Icon name="bx-game-regular" class="w-4 h-4 mr-1" /> Spielen
			</Button>
		</div>
	</div>
</Card>
