import { Component, OnInit } from '@angular/core';
import { WordleRow, LetterState, TodaysAnswerResponse, WordInfoRow } from '../row'
import { TodaysAnswerService } from '../todays-answer.service';

import * as alertifyjs from 'alertifyjs';

export interface WordInfoData {
  word: string;
  exp_info: number;
  word_freq: number;
  rank: number;
}

@Component({
  selector: 'app-todays-answer',
  templateUrl: './todays-answer.component.html',
  styleUrls: ['./todays-answer.component.css']
})
export class TodaysAnswerComponent implements OnInit {

  show_letters: boolean = false;
  answer: WordleRow[] = []
  share_text: string = ""
  word_info: WordInfoRow[] = []
  current_row_info: WordInfoRow | null = null;
  word_list: WordInfoData[] | null = null;

  constructor(private todays_answer: TodaysAnswerService ) {
  }

  ngOnInit(): void {
    this.todays_answer.loadRows().subscribe(answer_res => this.checkResponse(answer_res));
    //console.log(this.share_text);
    alertifyjs.set('notifier','position', 'top-center');
  }

  private checkResponse(answer_res: TodaysAnswerResponse) {
    console.log("Answer data loaded");
    console.log(answer_res.word_info);
    this.answer = answer_res.rows;
    this.share_text = answer_res.share_text;
    this.word_info = answer_res.word_info;
    while ( this.answer.length < 6 )
    {
      let l: LetterState[] = [];
      for ( let i = 0; i < 5; i++ )
      {
        let state: LetterState = {letter: '', state: 'column'}
        l.push(state);
      }
      let r: WordleRow = {letters: JSON.parse(JSON.stringify(l))}
      this.answer.push(r)
    }
  }

  rowSelect(row: number): void {
    if ( row < this.word_info.length ) {
      let data: WordInfoData[] = []
      for (let key in this.word_info[row].first_100) {
        let value = this.word_info[row].first_100[key];
        data.push({word: key, exp_info: value.exp_info, word_freq: value.word_freq, rank: value.rank})
      }
      this.current_row_info = this.word_info[row];
      this.word_list = data.sort((a, b) => (b.rank - a.rank));
    } else {
      this.current_row_info = null;
      this.word_list = null;
    }
    console.log("Row select " + row + " row " + this.current_row_info);
  }
  
  sortby(t: string) {
    if ( this.word_list != null ) {
      if ( t == 'info' ) {
        this.word_list = this.word_list.sort((a, b) => (b.exp_info - a.exp_info));
      } else {
        this.word_list = this.word_list.sort((a, b) => (b.rank - a.rank));
      }  
    }
  }

  share() {
    navigator.clipboard.writeText("Wobot " + this.share_text + "https://wobot.brsoft.io for complete solution");
    alertifyjs.success('Copied to clipboard');
  }

  toggleShow() {
    this.show_letters = !this.show_letters;
  }
}
