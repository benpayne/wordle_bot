import { Component, OnInit } from '@angular/core';
import { WordleRow, LetterState, TodaysAnswerResponse } from '../row'
import { TodaysAnswerService } from '../todays-answer.service';

@Component({
  selector: 'app-todays-answer',
  templateUrl: './todays-answer.component.html',
  styleUrls: ['./todays-answer.component.css']
})
export class TodaysAnswerComponent implements OnInit {

  show_letters: boolean = false;
  answer: WordleRow[] = []

  constructor(private todays_answer: TodaysAnswerService ) {
  }

  ngOnInit(): void {
    this.todays_answer.loadRows().subscribe(answer_res => this.checkResponse(answer_res));
    console.log(this.answer);
  }

  private checkResponse(answer_res: TodaysAnswerResponse) {
    console.log("done");
    console.log(answer_res.rows);
    this.answer = answer_res.rows;
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

  toggleShow() {
    this.show_letters = !this.show_letters;
  }
}
