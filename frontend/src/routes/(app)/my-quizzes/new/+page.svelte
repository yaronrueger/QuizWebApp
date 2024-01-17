<script lang="ts">
	import {
		Label,
		Input,
		Button,
		Textarea,
		Accordion,
		AccordionItem,
		Span,
		Range,
		Dropdown,
		Radio,
		Helper,
		Alert
	} from 'flowbite-svelte';
	import { Icon } from 'svelte-boxicons';
	import { get } from 'svelte/store';
	import axios, { AxiosError, isAxiosError } from 'axios';
	import { categoryMap, type Quiz } from '@config/navigation';
	import { accessToken, newQuiz } from '@config/stores';
	import { API_BASE_PATH } from '@config/api';

	const quizCategories = Object.keys(categoryMap);

	let categoryUsed = -1;
	let showAlert = false;

	function removeQuestion() {
		newQuiz.update((oldQuiz) => {
			if (oldQuiz.questions.length > 1) {
				return {
					...oldQuiz,
					questions: oldQuiz.questions.slice(0, oldQuiz.questions.length - 1)
				};
			}
			return oldQuiz;
		});
	}

	function addQuestion() {
		newQuiz.update((oldQuiz) => {
			return {
				...oldQuiz,
				questions: [
					...oldQuiz.questions,
					{
						title: '',
						points: 10,
						answers: ['', '', '', '']
					}
				]
			};
		});
	}

	async function onSubmit(event: Event) {
		event.preventDefault();
		const form = event.currentTarget as HTMLFormElement;
		const formData = new FormData(form);

		const quizName = formData.get('quizName')?.toString();
		const quizDescription = formData.get('quizDescription')?.toString();
		const quizCategory = categoryMap[formData.get('quizCategory')?.toString()!];

		const quizQuestions = formData.getAll('quizQuestions');
		const quizAnswers = formData.getAll('quizAnswers');
		const quizPoints = formData.getAll('quizPoints');

		function prepData() {
			// Create an object to store the questions with corresponding answers
			const questionAnswerObject: Quiz = {
				title: quizName!,
				desc: quizDescription!,
				category: quizCategory!,
				questions: []
			};

			// Loop through the questions and answers and create the desired object
			for (let i = 0; i < quizQuestions.length; i++) {
				const question = {
					title: quizQuestions[i].toString(),
					answers: [
						quizAnswers[i * 4].toString(),
						quizAnswers[i * 4 + 1].toString(),
						quizAnswers[i * 4 + 2].toString(),
						quizAnswers[i * 4 + 3].toString()
					],
					points: parseInt(quizPoints[i].toString())
				};
				questionAnswerObject.questions.push(question);
			}
			return questionAnswerObject;
		}

		const data = prepData();

		axios
			.post(`${API_BASE_PATH}/user/quiz`, data, {
				headers: {
					Authorization: 'Bearer ' + $accessToken
				}
			})
			.then((response) => {
				if (response.status === 200) {
					window.location.assign('/my-quizzes');
				} else {
				}
			})
			.catch((error) => {
				console.log(error);
				showAlert = true;
				if (isAxiosError(error)) {
					console.error((error as AxiosError).name);
				}
			});

		setTimeout(function () {
			showAlert = false;
		}, 3000);
	}
</script>

{#if showAlert}
	<Alert color="red" dismissable>
		Etwas ist schiefgelaufen. Überprüfe deine Eingaben und probiere es erneut.
	</Alert>
{/if}
<div class="w-full flex justify-center">
	<div class="w-full max-w-3xl">
		<h2 class="mb-4 text-3xl font-bold text-gray-900 dark:text-white">
			Neues Quiz erstellen
		</h2>
		<form method="post" id="quizForm" on:submit={onSubmit}>
			<div class="grid gap-4 sm:grid-cols-2 sm:gap-6">
				<div class="sm:col-span-2">
					<Label for="quizName" class="mb-2">Quiz Name *</Label>
					<Input name="quizName" type="text" id="name" placeholder="z.B. Tier Quiz" required />
				</div>
				<div class="sm:col-span-2">
					<Label for="description" class="mb-2">Quiz Beschreibung</Label>
					<Textarea
						id="description"
						name="quizDescription"
						placeholder="Beschreibung über welche Themen dein Quiz handelt"
						rows="4"
					/>
				</div>
			</div>
			<div class="float-left mb-2">
				<Label>Quiz Kategorie: *</Label>
				<Button size="xs"
					>{categoryUsed !== -1 ? quizCategories[categoryUsed] : 'Kategorie auswählen'}<Icon
						name="bx-chevron-down-regular"
						class="w-5 h-5"
					/></Button
				>
				<Dropdown class="w-48  space-y-1">
					{#each quizCategories as category, i}
						<li class="rounded p-2 hover:bg-gray-100 dark:hover:bg-gray-600">
							<Radio bind:group={categoryUsed} value={i}>{category}</Radio>
						</li>
					{/each}
				</Dropdown>
				<Input
					class="hidden"
					name="quizCategory"
					type="text"
					value={quizCategories[categoryUsed]}
				/>
			</div>
			<div class="float-right mt-5">
				<Button on:click={addQuestion} size="xs" title="Frage hinzufügen">
					<Icon name="bx-plus-regular" class="w-5 h-5" />
				</Button>
				<Button on:click={removeQuestion} size="xs" title="Frage löschen">
					<Icon name="bx-minus-regular" class="w-5 h-5" />
				</Button>
			</div>
			{#key $newQuiz.questions.length}
				<Accordion>
					{#each $newQuiz.questions as question}
						<AccordionItem open>
							<span slot="header">Frage {$newQuiz.questions.indexOf(question) + 1}</span>
							<div slot="arrowup">
								<Icon name="bx-up-arrow-regular" class="h-5 w-5 -mr-0.5" />
							</div>
							<span slot="arrowdown">
								<Icon name="bx-down-arrow-regular" class="h-5 w-5 -mr-0.5" />
							</span>
							<div class="grid gap-4 sm:grid-cols-2 sm:gap-6">
								<div class="sm:col-span-2">
									<Label for="question" class="mb-2"
										>{$newQuiz.questions.indexOf(question) + 1}. Frage *</Label
									>
									<Input
										type="text"
										name="quizQuestions"
										bind:value={question.title}
										id="name"
										placeholder="Deine Frage"
										autocomplete="off"
										required
									/>
								</div>
								<div class="w-full">
									<Label for="firstAnswer" class="mb-2"
										><Span highlightClass="dark:text-green-500" highlight>Richtige</Span> Antwort *</Label
									>
									<Input
										bind:value={question.answers[0]}
										name="quizAnswers"
										type="text"
										id="firstAnswer"
										placeholder="Antwortmöglichkeit"
										autocomplete="off"
										required
									/>
								</div>
								<div class="w-full">
									<Label for="secondAnswer" class="mb-2"
										><Span highlightClass="dark:text-red-500" highlight>Falsche</Span> Antwort *</Label
									>
									<Input
										bind:value={question.answers[1]}
										name="quizAnswers"
										type="text"
										id="secondAnswer"
										placeholder="Antwortmöglichkeit"
										autocomplete="off"
										required
									/>
								</div>
								<div class="w-full">
									<Label for="thirdAnswer" class="mb-2"
										><Span highlightClass="dark:text-red-500" highlight>Falsche</Span> Antwort *</Label
									>
									<Input
										bind:value={question.answers[2]}
										name="quizAnswers"
										type="text"
										id="thirdAnswer"
										placeholder="Antwortmöglichkeit"
										autocomplete="off"
										required
									/>
								</div>
								<div class="w-full">
									<Label for="fourthAnswer" class="mb-2"
										><Span highlightClass="dark:text-red-500" highlight>Falsche</Span> Antwort *</Label
									>
									<Input
										bind:value={question.answers[3]}
										autocomplete="off"
										name="quizAnswers"
										type="text"
										id="fourthAnswer"
										placeholder="Antwortmöglichkeit"
										required
									/>
								</div>
							</div>
							<div class="mt-1">
								<Label>Punktzahl</Label>
								<Range
									name="quizPoints"
									id="range-steps"
									min="5"
									max="25"
									bind:value={question.points}
									step="5"
								/>
								<p>{question.points} Punkte</p>
							</div>
						</AccordionItem>
					{/each}
				</Accordion>
			{/key}
			<Helper class="text-sm mb-5">
				<!-- svelte-ignore a11y-missing-attribute -->
				Alle mit "*" gekennzeichneten Felder sind
				<a class="font-medium text-primary-600 hover:underline dark:text-primary-500">
					verpflichtend
				</a>
				.
			</Helper>

			<Button type="submit" class="w-40">Quiz erstellen</Button>
		</form>
	</div>
</div>
