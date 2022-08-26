export interface LetterState {
    letter: string;
    state: string;
}

export interface WordleRow {
    letters: LetterState[];
}

export interface WordListResponse {
    res: string;
    words: string[];
}

export interface WinningWordResponse {
    res: string;
    winning_word: string;
}

export interface TodaysAnswerResponse {
    res: string;
    rows: WordleRow[];
}

export interface NewAnswerResponse {
    res: string;
    word: string;
}