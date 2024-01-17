<script lang="ts">
	import { Button, Checkbox, Dropdown, Heading, Search } from 'flowbite-svelte';
	import QuizExploreCard from '@component/User/quizExploreCard.svelte';
	import { categoryMap, type Quiz, type quizInfo } from '@config/navigation';
	import axios from 'axios';
	import { API_BASE_PATH } from '@config/api';
	import { onMount } from 'svelte';
	import { Icon } from 'svelte-boxicons';
	import { accessToken } from '@config/stores';

	let data: quizInfo[] = [];
	let categoryFilter: number[] = [];
	let searchString: string = '';

	const config = {
		headers: { Authorization: `Bearer ${$accessToken}` }
	};

	function addFilter(newValue: number) {
		categoryFilter = [...categoryFilter, newValue];
	}

	function removeFilter(valueToRemove: number) {
		categoryFilter = categoryFilter.filter((v) => v !== valueToRemove);
	}

	function clearFilter() {
		categoryFilter = [];
	}

	async function loadData() {
		await axios.get(`${API_BASE_PATH}/quizzes`, config).then((response) => {
			data = response.data.Quizes;
		});

		for (let i = 0; i < data.length; i++) {
			await axios
				.get(`${API_BASE_PATH}/quizzes/quiz/bestlist/user?quiz_id=${data[i].id}`, config)
				.then((response) => {
					data[i].points_percentage = response.data.points_percentage;
				});
		}
	}

	const onFilterChange = (event: Event) => {
		const input = event.currentTarget as HTMLInputElement;
		const category = parseInt(input.getAttribute('data-category') || '0');
		if (input && input.checked) addFilter(category);
		if (input && !input.checked) removeFilter(category);
	};

	const onSearchChange = (event: Event) => {
		const input = event.currentTarget as HTMLInputElement;
		searchString = input.value;
	};

	onMount(() => {
		loadData();
	});

	function filterCategoryAndSearchString(
		searchString: string,
		categoryFilter: number[],
		data: quizInfo[]
	): quizInfo[] {
		data = data;
		if (categoryFilter.length > 0) {
			data = data.filter((quiz) => categoryFilter.includes(quiz.category));
		}
		if (searchString !== '') {
			data = data.filter(
				(quiz) =>
					quiz.title.startsWith(searchString) ||
					quiz.desc.startsWith(searchString) ||
					quiz.title.includes(searchString) ||
					quiz.desc.includes(searchString)
			);
		}
		return data;
	}

	$: filteredData = filterCategoryAndSearchString(searchString, categoryFilter, data);
</script>

<Heading class="pl-8 pt-8" tag="h1" customSize="text-3xl">Quizze entdecken</Heading>
<div class="w-full">
	<div class="flex gap-3 mb-6 pl-8 pt-4">
		<div class="max-w-xl">
			<Search on:change={onSearchChange} />
		</div>
		<Button>Kategorie<Icon name="bx-chevron-down-regular" class="w-5 h-5" /></Button>
		<Dropdown class="w-44 p-3 space-y-3 text-sm">
			{#each Object.keys(categoryMap) as value}
				<li>
					<Checkbox
						checked={categoryFilter.includes(categoryMap[value])}
						on:change={onFilterChange}
						data-category={categoryMap[value]}
					>
						{value}
					</Checkbox>
				</li>
			{/each}
		</Dropdown>
		{#if categoryFilter.length !== 0}
			<Button on:click={clearFilter} color="alternative">
				<Icon name="bx-trash-regular" class="w-5 h-5" />
				Clear
			</Button>
		{/if}
	</div>

	<div class="grid grid-cols-5 md:grid-cols-3 sm:grid-cols-2 xs:grid-cols-1 gap-4 mx-10">
		{#each filteredData as quiz}
			<QuizExploreCard {quiz} />
		{/each}
	</div>
</div>
