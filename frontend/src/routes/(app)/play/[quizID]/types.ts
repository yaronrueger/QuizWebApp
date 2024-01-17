export type ShuffledQuestion = {
	id: number;
	quiz_id: number;
	title: string;
	answers: string[];
	realAnswerId: number[];
	points: number;
};

export interface questionObject {
	Questions: ShuffledQuestion[];
}
