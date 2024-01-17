<script lang="ts">
	import {
		Button,
		Card,
		Heading,
		Span,
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell
	} from 'flowbite-svelte';
	import InfoCard from '@component/Home/infoCard.svelte';
	import CreatedQuizzesInfo from '@component/Home/createdQuizzesInfo.svelte';
	import { onMount } from 'svelte';
	import { API_BASE_PATH } from '@config/api';
	import axios from 'axios';
	import { accessToken } from '@config/stores';
	import { Icon } from 'svelte-boxicons';
	import { generateRanks, type UserRank } from '@config/navigation';

	let userInfo = {
		completedQuizzes: 0,
		allPoints: 0
	};
	let userQuizFacts = {
		createdQuizzes: 0,
		quizUser: 0
	};

	const config = {
		headers: { Authorization: `Bearer ${$accessToken}` }
	};

	let userData: { id: number; username: string } = { id: 0, username: '' };

	let ranking: UserRank[] = [];

	let quizTitle: string = '';
	let quizID: number = -1;

	onMount(async () => {
		await loadData();
		await getRandomRanking();
		await getInformation();
	});

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

	async function getRandomRanking() {
		try {
			const response = await axios.get(`${API_BASE_PATH}/quizzes/ids`, config);
			const randomIndex = Math.floor(Math.random() * response.data.IDs.length);
			const randomQuizID = response.data.IDs[randomIndex];

			const title = await axios.get(
				`${API_BASE_PATH}/quizzes/quiz?quiz_id=${randomQuizID}`,
				config
			);

			quizTitle = title.data.title;
			quizID = randomQuizID;

			const ratingResponse = await axios.get(
				`${API_BASE_PATH}/quizzes/quiz/bestlist?quiz_id=${randomQuizID}`,
				config
			);
			ranking = generateRanks(ratingResponse.data);

			return mapMedals(ranking);
		} catch (error) {
			console.log(error);
		}
	}

	async function getInformation() {
		try {
			const data = await axios.get(`${API_BASE_PATH}/user/landingpageinformation`, config);

			userInfo = {
				completedQuizzes: data.data.played_quizzes,
				allPoints: data.data.collected_points
			};

			userQuizFacts = {
				createdQuizzes: data.data.created_quizzes,
				quizUser: data.data.quiz_plays
			};
		} catch (error) {}
	}

	async function loadData() {
		axios
			.get(`${API_BASE_PATH}/user/me`, config)
			.then((response) => {
				userData = {
					id: response.data.id,
					username: response.data.username
				};
				return userData;
			})
			.catch((error) => {
				console.log(error);
			});
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

	let username: Promise<string> = getUserName();
</script>

<Heading
	tag="h1"
	class="mt-4 mb-24 text-center"
	customSize="text-4xl font-extrabold  md:text-5xl lg:text-6xl"
	>Willkommen <Span gradient>{userData.username}</Span></Heading
>
<div class="grid gap-16 grid-cols-3 mx-6 max-h-96">
	<InfoCard {userInfo} />
	<CreatedQuizzesInfo {userQuizFacts} />
	<Card class="flex w-fit" size="lg">
		<h5 class="mb-6 text-3xl font-bold tracking-tight text-gray-900 dark:text-white">
			Bestenliste🎯: {quizTitle}
		</h5>
		<Table class="w-full h-full" striped={true} table-fixed>
			<TableHead>
				<TableHeadCell class="w-1/3">Rang</TableHeadCell>
				<TableHeadCell class="w-1/3">Name</TableHeadCell>
				<TableHeadCell class="w-1/3">Punkte</TableHeadCell>
			</TableHead>
			{#await username then name}
				<TableBody>
					{#each ranking.slice(0, 4) as record}
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
		<div class="flex justify-between mt-3">
			<Button href="/ranking/{quizID}" color="alternative">
				<Icon name="bx-list-ol-regular" class="w-4 h-4 mr-1" /> Bestenliste
			</Button>
			<Button href="/play/{quizID}">
				<Icon name="bx-game-regular" class="w-4 h-4 mr-1" /> Spielen
			</Button>
		</div>
	</Card>
</div>
