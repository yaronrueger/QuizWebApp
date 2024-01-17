<script lang="ts">
	import { page } from '$app/stores';
	import { Heading } from 'flowbite-svelte';
	$: quizId = $page.params.id;
</script>

<Heading>Quiz Id: {quizId}</Heading>
