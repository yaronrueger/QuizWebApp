<script lang="ts">
	import {
		Button,
		Modal,
		Span,
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell
	} from 'flowbite-svelte';
	import type { questionObject } from './types';
	import { Icon } from 'svelte-boxicons';

	export let showModal: boolean;
	export let quiz: questionObject['Questions'];
	export let achievedPoints: number;
	export let possiblePoints: number;
	export let answerCorrect: boolean[];
	export let quizTitle: string;
</script>

<Modal title="Geschafft!" bind:open={showModal}>
	<p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
		Du hast erfolgreich das Quiz: <Span highlight>{quizTitle}</Span> abgeschlossen. Dabei hast du
		<Span highlight>{achievedPoints}</Span> von <Span highlight>{possiblePoints}</Span> Punkte erreicht.
	</p>
	<Table>
		<TableHead>
			<TableHeadCell>Frage</TableHeadCell>
			<TableHeadCell>Mögiche Punkte</TableHeadCell>
			<TableHeadCell>Korrekt?</TableHeadCell>
		</TableHead>
		<TableBody>
			{#each quiz as question, i}
				<TableBodyRow>
					<TableBodyCell>{question.title}</TableBodyCell>

					<TableBodyCell>{question.points}</TableBodyCell>
					{#if answerCorrect[i]}
						<TableBodyCell
							><Icon name="bx-check-regular" class="w-5 h-5 bg-green-400" /></TableBodyCell
						>
					{:else}
						<TableBodyCell><Icon name="bx-x-regular" class="w-5 h-5 bg-red-600" /></TableBodyCell>
					{/if}
				</TableBodyRow>
			{/each}
		</TableBody>
	</Table>
	<svelte:fragment slot="footer">
		<Button href="/">Zurück zum Hauptmenü</Button>
	</svelte:fragment>
</Modal>
