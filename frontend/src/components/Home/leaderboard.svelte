<script lang="ts">
	import { page } from '$app/stores';
	import { API_BASE_PATH } from '@config/api';
	import { type UserRank, type UserScore, generateRanks } from '@config/navigation';
	import { accessToken } from '@config/stores';
	import axios from 'axios';
	import {
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell
	} from 'flowbite-svelte';

	const config = {
		headers: { Authorization: `Bearer ${$accessToken}` }
	};

	const quizID = $page.params.quizID;

	function mapMedals(ranking: UserRank[]): UserRank[] {
		ranking.forEach((obj) => {
			switch (obj.rank) {
				case 1:
					obj.rank = '🥇';
					break;
				case 2:
					obj.rank = '🥈';
					break;
				case 3:
					obj.rank = '🥉';
					break;
				default:
					obj.rank = obj.rank;
			}
		});
		return ranking;
	}

	async function getRankingData(): Promise<UserRank[]> {
		let data: UserScore[] = [];
		try {
			await axios
				.get(`${API_BASE_PATH}/quizzes/quiz/bestlist?quiz_id=${quizID}`, config)
				.then((response) => {
					data = response.data;
				})
				.catch((error) => {
					console.log(error);
				});
		} catch (error) {
			console.log(error);
		}

		const finalData = generateRanks(data);
		return mapMedals(finalData);
	}

	async function getUserName(): Promise<string> {
		let name: string = '';
		try {
			await axios
				.get(`${API_BASE_PATH}/user/me`, config)
				.then((response) => {
					name = response.data.username;
				})
				.catch((error) => {
					console.log(error);
				});
		} catch (error) {
			console.log(error);
		}
		return name;
	}

	let rankingData: Promise<UserRank[]> = getRankingData();
	let username: Promise<string> = getUserName();
</script>

{#await rankingData then ranking}
	<div class="w-fit flex flex-col justify-center content-center">
		<Table class="w-full h-full" table-fixed shadow>
			<TableHead>
				<TableHeadCell class="w-1/3">Rang</TableHeadCell>
				<TableHeadCell class="w-1/3">Name</TableHeadCell>
				<TableHeadCell class="w-1/3">Punkte</TableHeadCell>
			</TableHead>
			{#await username then name}
				<TableBody>
					{#each ranking as record}
						{#if record.username !== name}
							<TableBodyRow>
								<TableBodyCell><p class="text-lg text-center">{record.rank}</p></TableBodyCell>
								<TableBodyCell><p class="text-lg text-center">{record.username}</p></TableBodyCell>
								<TableBodyCell><p class="text-lg text-center">{record.points}</p></TableBodyCell>
							</TableBodyRow>
						{:else}
							<TableBodyRow>
								<TableBodyCell
									><p class="text-primary-500 text-lg text-center">{record.rank}</p></TableBodyCell
								>
								<TableBodyCell
									><p class="text-primary-500 text-lg text-center">
										{record.username}
									</p></TableBodyCell
								>
								<TableBodyCell
									><p class="text-primary-500 text-lg text-center">
										{record.points}
									</p></TableBodyCell
								>
							</TableBodyRow>
						{/if}
					{/each}
				</TableBody>
			{/await}
		</Table>
	</div>
{/await}
