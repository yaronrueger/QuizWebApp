export type NavigationItem = { icon: string; label: string; href: string };

export const NAVIGATION_ITEMS: NavigationItem[] = [
	{ icon: 'bx-home-alt-2-regular', label: 'Home', href: '/' },
	{ icon: 'bx-compass-regular', label: 'Alle Quizze', href: '/explore' },
	{ icon: 'bx-cabinet-regular', label: 'Meine Quizze', href: '/my-quizzes' },
	// Auskommentiert, da Bestenliste nur für jedes Quiz über Explore erreichbar
	// { icon: 'bx-list-ol-regular', label: 'Bestenliste', href: '/ranking' },
	{ icon: 'bx-plus-regular', label: 'Neues Quiz erstellen', href: '/my-quizzes/new' }
];

export const SECONDARY_NAVIGATION_ITEMS: NavigationItem[] = [
	{ icon: 'bx-user-regular', label: 'Benutzer', href: '/user' },
	{ icon: 'bx-log-out-regular', label: 'Abmelden', href: '/login' }
];

export type Quiz = { title: string; desc: string; questions: question[]; category: number };

export type quizInfo = {
	id: number;
	creator: number;
	title: string;
	desc: string;
	category: number;
	created: string;
	modified: string;
	plays: number;
	points_percentage: number;
};

export type QuizByID = {
	id: number;
	creator: number;
	title: string;
	desc: string;
	category: number;
	created: string;
	modified: string;
	plays: number;
};

export type question = {
	id: number;
	quiz_id: number;
	title: string;
	answers: string[];
	points: number;
};

export const categoryMap: { [key: string]: number } = {
	'Literatur und Bücher': 0,
	Geschichte: 1,
	'Wissenschaft und Technologie': 2,
	'Film und Fernsehen': 3,
	Musik: 4,
	'Politik und Gesellschaft': 5,
	Geografie: 6,
	Sport: 7,
	Popkultur: 8,
	'Wissenschaftliche Erfindungen': 9,
	Anders: 10
};

export type UserScore = [string, number];
export type UserRank = { username: string; points: number; rank: number | string };

export function generateRanks(userScores: UserScore[]): UserRank[] {
	let rank = 1;
	let previousPoints: number | null = null;

	return userScores.map(([username, points], index) => {
		// If this user has the same points as the previous one, they get the same rank.
		// Otherwise, the rank is equal to the current array index + 1 (since 1-indexed).
		if (points !== previousPoints) rank = index + 1;

		previousPoints = points;

		return { username, points, rank };
	});
}
