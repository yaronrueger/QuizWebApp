<script lang="ts">
	import { Button, Card } from 'flowbite-svelte';
	import axios from 'axios';
	import { accessToken } from '../../../../config/stores';
	import { page } from '$app/stores';
	import { API_BASE_PATH } from '@config/api';
	import type { ShuffledQuestion, questionObject } from './types';
	import QuizCompleteModal from './QuizCompleteModal.svelte';
	import type { question } from '@config/navigation';

	const config = {
		headers: { Authorization: `Bearer ${$accessToken}` }
	};

	let currentQuestion = 0;
	let group = -1;
	let showModal = false;
	let quizTitle = '';
	let answerCorrect: boolean[] = [];
	let achievedPoints: number = 0;
	let possiblePoints: number = 0;

	let quizData: Promise<questionObject['Questions']> = getQuiz();

	async function getQuiz(): Promise<questionObject['Questions']> {
		const quizID = $page.params.quizID;

		let data = [
			{
				id: 0,
				title: '',
				points: 0,
				quiz_id: 0,
				answers: ['', '', '', ''],
				realAnswerId: [0, 1, 2, 3]
			}
		];

		try {
			await axios
				.get(`${API_BASE_PATH}/quizzes/quiz/questions?quiz_id=${quizID}`, config)
				.then((response) => {
					data = response.data.Questions.map((question: ShuffledQuestion) => {
						question.realAnswerId = shuffleArray([0, 1, 2, 3]);
						return question;
					});
				})
				.catch((error) => {
					console.log(error);
				});
		} catch (error) {
			console.log(error);
		}
		return data;
	}

	async function handleClick(event: Event) {
		const button = event.currentTarget as HTMLButtonElement;
		const value = button.getAttribute('data-value');
		group = parseInt(value ?? '-1');

		console.log('Question:', (await quizData).length, 'Current:', currentQuestion);

		if ((await quizData).length - 1 <= currentQuestion) {
			console.log('This is the end 🎵');
			handleEnd();
			return;
		}

		await checkAnswer();

		group = -1;
	}

	async function handleEnd() {
		(await quizData).forEach((question: question) => {
			possiblePoints += question.points;
		});

		await checkAnswer();

		await axios
			.get(
				`${API_BASE_PATH}/quizzes/quiz/bestlist/user/points?quiz_id=${$page.params.quizID}`,
				config
			)
			.then((response) => {
				achievedPoints = response.data.points;
				possiblePoints = response.data.possible;
			});

		if (group >= 0) {
			await axios
				.get(`${API_BASE_PATH}/quizzes/quiz?quiz_id=${$page.params.quizID}`, config)
				.then((response) => {
					quizTitle = response.data.title;
				})
				.catch((error) => {
					console.log(error);
				});
		}

		showModal = true;
	}

	async function checkAnswer() {
		const body = { question: (await quizData)[currentQuestion].id, chosen: group };

		if (group >= 0) {
			await axios
				.post(`${API_BASE_PATH}/user/check_answer`, body, config)
				.then((response) => {
					answerCorrect.splice(currentQuestion, 0, response.data.output);
				})
				.catch((error) => {
					console.log(error);
				});

			currentQuestion < (await quizData).length - 1 ? currentQuestion++ : null;
		}
	}

	// Ref: https://www.educative.io/answers/how-to-shuffle-an-array-in-javascript
	function shuffleArray(array: number[]): number[] {
		const newArray = array.slice(0);
		let len = newArray.length;
		let currentIndex = len;
		for (currentIndex = len - 1; currentIndex > 0; currentIndex--) {
			let randIndex = Math.floor(Math.random() * (currentIndex + 1));
			var temp = newArray[currentIndex];
			newArray[currentIndex] = newArray[randIndex];
			newArray[randIndex] = temp;
		}
		return newArray;
	}

	$: console.log({
		currentQuestion,
		group,
		showModal,
		quizTitle,
		answerCorrect,
		achievedPoints,
		possiblePoints
	});
</script>

{#await quizData then questions}
	<div class="w-full flex items-center flex-col">
		<Card class="w-full max-w-2xl">
			<!-- {JSON.stringify(questions)} -->
			<h6 class="mb-1 text-5xl font-bold tracking-tight text-gray-900 dark:text-white text-center">
				{questions[currentQuestion].title}
			</h6>
			<p class="text-center mt-1">{questions[currentQuestion].points} Punkte</p>
			<div class="grid gap-2 sm:grid-cols-2 sm:gap-2 mt-6">
				{#each questions[currentQuestion].realAnswerId as index, realIndex}
					<Button
						on:click={handleClick}
						data-value={index}
						size="xl"
						color={['blue', 'red', 'yellow', 'green'][realIndex]}
					>
						{questions[currentQuestion].answers[index]}
					</Button>
				{/each}
			</div>
			<div class="grid gap-4 sm:grid-cols-2 sm:gap-6 mt-3">
				<p class="flex justify-start items-center">{currentQuestion + 1}/{questions.length}</p>
			</div>
		</Card>
	</div>
	<QuizCompleteModal
		bind:showModal
		{achievedPoints}
		{answerCorrect}
		{possiblePoints}
		{quizTitle}
		quiz={questions}
	/>
{/await}
