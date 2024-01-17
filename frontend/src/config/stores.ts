import { get, writable, type Writable } from 'svelte/store';
import type { Quiz } from './navigation';
import { browser } from '$app/environment';


// Ref: https://stackoverflow.com/questions/56488202/how-to-persist-svelte-store
const storage = <T>(key: string, initValue: T): Writable<T> => {
	const store = writable(initValue);
	if (!browser) return store;

	const storedValueStr = localStorage.getItem(key);
	if (storedValueStr != null) store.set(JSON.parse(storedValueStr));

	store.subscribe((val: T) => {
		if (val === undefined || val === null) {
			localStorage.removeItem(key);
		} else {
			localStorage.setItem(key, JSON.stringify(val));
		}
	});

	window.addEventListener('storage', () => {
		const storedValueStr = localStorage.getItem(key);
		if (storedValueStr == null) return;

		const localValue: T = JSON.parse(storedValueStr);
		if (localValue !== get(store)) store.set(localValue);
	});

	return store;
};

export const newQuiz = writable<Quiz>({
	title: '',
	desc: '',
	questions: [
		{
			title: '',
			answers: ['', '', '', ''],
			points: 10
		}
	],
	category: 0
});

export const accessToken = storage<string|undefined>('app:token', '');
