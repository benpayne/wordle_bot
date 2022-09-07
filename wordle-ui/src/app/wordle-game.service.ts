import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { WordleRow, LetterState, WordListResponse, NewAnswerResponse } from './row';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WordleGameService {

  current_row: number = 0;
  current_column: number = 0;
  winning_word: string = "cares";
  word_list: string[] = [];
  game_done = false;
  keyboard = new Map<string, string>();

  private word_list_url = '/game/word_list';
  private new_answer_url = '/game/start';

  rows: WordleRow[] = []

  keyboard_layout: string[][][] = [
    [['q', ''], ['w', ''], ['e', ''], ['r', ''], ['t', ''], ['y', ''], ['u', ''], ['i', ''], ['o', ''], ['p', '']],
    [['a', ''], ['s', ''], ['d', ''], ['f', ''], ['g', ''], ['h', ''], ['j', ''], ['k', ''], ['l', '']],
    [['enter', 'letter-wide'], ['z', ''], ['x', ''], ['c', ''], ['v', ''], ['b', ''], ['n', ''], ['m', ''], ['back', 'letter-wide']]
  ];

  constructor(private http: HttpClient) 
  {
    let data = localStorage.getItem('wordle-data');
    if ( data ) {
      console.log("found persistent data, loading...");
      this.rows = JSON.parse(data);
      let keyboard = localStorage.getItem('wordle-data-keyboard');
      if (keyboard) {
        this.keyboard_layout = JSON.parse(keyboard);
      }
      let row = localStorage.getItem('wordle-data-row');
      if (row) {
        this.current_row = JSON.parse(row);
      }
      let column = localStorage.getItem('wordle-data-column');
      if (column) {
        this.current_column = JSON.parse(column);
      }
      let winning = localStorage.getItem('wordle-data-winning');
      if (winning) {
        this.winning_word = JSON.parse(winning);
      }
      let game_done = localStorage.getItem('wordle-data-done');
      if (game_done) {
        this.game_done = JSON.parse(game_done);
      }

      console.log("row: " + this.current_row + " column: " + this.current_column);
    } else {
      this.reset();
      console.log("generating default data" + this.rows);
    }
    this.loadWordList().subscribe(word_res => this.word_list = word_res.words);
  }

  saveRowData(): void {
    localStorage.setItem('wordle-data', JSON.stringify(this.rows));
    localStorage.setItem('wordle-data-keyboard', JSON.stringify(this.keyboard_layout));
    localStorage.setItem('wordle-data-row', JSON.stringify(this.current_row));
    localStorage.setItem('wordle-data-column', JSON.stringify(this.current_column));
    localStorage.setItem('wordle-data-winning', JSON.stringify(this.winning_word));
    localStorage.setItem('wordle-data-done', JSON.stringify(this.game_done));
  }

  getRows(): WordleRow[] {
    return this.rows;
  }

  getKeyboard(): string[][][] {
    return this.keyboard_layout;
  }

  getWinningWord(): string {
    return this.winning_word;
  }

  getWordList(): string[] {
    return this.word_list;
  }

  checkWord(guess: string): boolean {
    console.log("guess is " + guess );
    console.log("Word list size " + this.word_list.length );
    if ( this.word_list.includes(guess) ) {
      return true;
    } else {
      return false;
    }
  }

  loadWordList(): Observable<WordListResponse> {
    return this.http.get<WordListResponse>(this.word_list_url);
  }

  loadNewAnswer(): Observable<NewAnswerResponse> {
    return this.http.get<NewAnswerResponse>(this.new_answer_url);
  }

  getGameDone(): boolean {
    return this.game_done;
  }

  updateKeyoard(): void {
    console.log("update keyboard");
    for ( const row of this.keyboard_layout ) {
      for ( const key of row ) {
        if ( key[0].length == 1 ) {
          let klass = this.checkLetter(key[0]);
          if ( klass != 'column' ) {
            console.log("setting class for " + key[0] + " to " + klass );
            key[1] = "letter-" + klass;
          }
        }
      }
    }
    this.saveRowData();
  }

  handleNewAnswer(answer_res: NewAnswerResponse): void {
    console.log(answer_res);
    if ( answer_res.res == "OK" ) {
      this.winning_word = answer_res.word
    }
  }

  reset(): void {
    this.current_row = 0;
    this.current_column = 0;
    this.loadNewAnswer().subscribe(answer_res => this.handleNewAnswer(answer_res));
    this.rows = [];
    this.game_done = false;
    let l: LetterState[] = [];
    for ( let i = 0; i < 5; i++ )
    {
      let state: LetterState = {letter: '', state: 'column'}
      l.push(state);
    }
    for ( let i = 0; i < 6; i++ )
    {
      let r: WordleRow = {letters: JSON.parse(JSON.stringify(l))}
      this.rows.push(r)
    }
    for ( const row of this.keyboard_layout ) {
      for ( const key of row ) {
        if ( key[0].length == 1 ) {
          key[1] = "";
        }
      }
    }
    this.keyboard = new Map<string, string>();
    this.saveRowData();
  }

  pushKey(letter: string): void {
    if ( this.current_column < 5 ) {
      this.rows[this.current_row].letters[this.current_column].letter = letter;
      this.current_column += 1
      this.saveRowData();
    }
  }

  popKey(): void {
    if ( this.current_column > 0 ) {
      this.current_column -= 1
      this.rows[this.current_row].letters[this.current_column].letter = '';  
      this.saveRowData();
    }
  }

  isRowComplete(): boolean {
    return this.current_column == 5;
  }

  currentWord(): string {
    let word = this.rows[this.current_row].letters[0].letter +
    this.rows[this.current_row].letters[1].letter +
    this.rows[this.current_row].letters[2].letter +
    this.rows[this.current_row].letters[3].letter +
    this.rows[this.current_row].letters[4].letter
    return word;
  }

  completeRow(): boolean {
    this.current_row += 1;
    if ( this.current_row < 6 ) {
      this.current_column = 0
      this.saveRowData();
      return true;
    } else {
      this.game_done = true;
      this.saveRowData();
      return false;
    }
  }

  checkLetter(c: string): string {
    let res = 'column';
    if ( this.keyboard.has(c) && typeof this.keyboard.get(c) === "string" ) {
      res = this.keyboard.get(c) as string;
    } else {
      return 'column';
    }
    return res;
  }

  compareGuess(guess: string): boolean {
    let result: string[] = ['absent', 'absent', 'absent', 'absent', 'absent'];
    // letters in the winning word, but not in correct position
    let letters: string[] = [];
    
    for (let i = 0; i < guess.length; i++) {
      const character = guess.charAt(i);
      if ( this.winning_word[i] == character ) {
        result[i] = 'correct'
        this.keyboard.set(character, 'correct')
      } else {
        letters.push(this.winning_word[i])
      }
    }

    for (let i = 0; i < guess.length; i++) {
      const character = guess.charAt(i);
      if ( result[i] == 'absent' ) {
        if ( letters.includes(character) ) {
          result[i] = 'present'
          if ( this.keyboard.get(character) != 'correct' ) {
            this.keyboard.set(character, 'present' )
          }
          // remove character from letters
          const index = letters.indexOf(character, 0);
          if (index > -1) {
            letters.splice(index, 1);
          }
        } else {
          this.keyboard.set(character, 'absent' )
        }
      }
    }

    let row: LetterState[] = []
    let done = true;
    for (let i = 0; i < guess.length; i++) {
      row.push({letter: guess.charAt(i), state: result[i]})
      if ( result[i] != 'correct'){
        done = false;
      }
    }

    this.rows[this.current_row].letters = row;
    this.game_done = done;
    this.saveRowData();

    return done;
  }
}

