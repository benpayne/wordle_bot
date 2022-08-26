import { Component, OnInit } from '@angular/core';
import { WordleRow, LetterState } from '../row';
import { HostListener } from '@angular/core';
import { WordleGameService } from '../wordle-game.service';

import * as alertifyjs from 'alertifyjs';


@Component({
  selector: 'app-play-wordle',
  templateUrl: './play-wordle.component.html',
  styleUrls: ['./play-wordle.component.css']
})
export class PlayWordleComponent implements OnInit {

  game_done = false;
  rows: WordleRow[] = [];
  keyboard_layout: string[][][] = [];

  constructor(private gameService: WordleGameService) {
    console.log("component constructor()");
  }

  ngOnInit(): void {
    alertifyjs.set('notifier','position', 'top-center');
    console.log("ngOnInit()" + this.gameService.game_done);
    if ( this.gameService.getGameDone() )
    {
      console.log("resetting completed game");
      this.resetGame(false);
    }
    this.rows = this.gameService.getRows();
    this.keyboard_layout = this.gameService.getKeyboard();
  }

  onKey(event: Event): void {
    if ( this.game_done == false ) {
      let elementId: string = (event.target as Element).id;
      let letter: string = elementId.split('_')[1];
      if ( letter == 'back' ) {
        this.gameService.popKey()
      } else if ( letter == 'enter' ) {
        this.processEnter()
      } else {
        this.gameService.pushKey(letter)
      }
    }
  }

  processEnter(): void {
    if ( this.gameService.isRowComplete() == false ) {
      alertifyjs.success('Not enought letters');
    } else {
      let word = this.gameService.currentWord();
      if (this.gameService.checkWord(word) == false){
        alertifyjs.success('Not a valid word ' + word);
      } else {
        console.log("Current word is " + word)
        if ( this.gameService.compareGuess(word) ) {
          alertifyjs.success('Congrats you win!!!');
          this.game_done = true;
        } else {
          this.game_done = !this.gameService.completeRow()
          if ( this.game_done ) {
            alertifyjs.success('Sorry you failed, the word was ' + this.gameService.getWinningWord());
            this.game_done = true;
          }
        }  
        this.gameService.updateKeyoard();
      }
    }
  }

  resetGame(notify = true): void {
    this.game_done = false;
    this.gameService.reset();
    this.rows = this.gameService.getRows()
    if ( notify ) {
      alertifyjs.success('Starting over');
    }
  }

  @HostListener('document:keypress', ['$event'])
  handleKeyboardEvent(event: KeyboardEvent) {
    if ( this.game_done == false ) {
      if (event.key >= 'a' && event.key <= 'z') {
        this.gameService.pushKey(event.key)
      } else if (event.key == 'Backspace' ) {
        this.gameService.popKey();
      } else if (event.key == 'Enter' ) {
        this.processEnter()
      } else {
        console.log(event.key)
      }
    }
  }
}
