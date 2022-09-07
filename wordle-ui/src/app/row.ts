export interface LetterState {
    letter: string;
    state: string;
}

export interface WordleRow {
    letters: LetterState[];
}

export interface WordInfo {
    exp_info: number;
    word_freq: number;
    rank: number;
}

export interface WordInfoRow {
    total_words: number;
    actual_info: number;
    total_info: number;
    first_100: {[word: string]: WordInfo}
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
    share_text: string;
    word_info: WordInfoRow[];
}

export interface NewAnswerResponse {
    res: string;
    word: string;
}

export interface FirstWordInfo {
    position: number;
    word: string;
    exp_info: number;
    word_weight: number;
}

export interface FirstWordResponse {
    res: string;
    words: FirstWordInfo[];
}