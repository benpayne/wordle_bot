import { Component, ComponentFactoryResolver, OnInit } from '@angular/core';
import { FirstWordService } from '../first-word.service';
import { FirstWordInfo, FirstWordResponse } from '../row';

@Component({
  selector: 'app-first-word',
  templateUrl: './first-word.component.html',
  styleUrls: ['./first-word.component.css']
})
export class FirstWordComponent implements OnInit {

  word_list: FirstWordInfo[] = [];
  top_word_list: FirstWordInfo[] = [];
  added_word_list: FirstWordInfo[] = [];
  word_list_name: string = "all";
  firstWord: string = '';
  sort_order: string = 'exp_info';

  constructor(private firstWordService: FirstWordService) { }

  ngOnInit(): void {
    this.firstWordService.loadFirstWordList(this.word_list_name, this.sort_order).subscribe(response => this.checkResponse(response));
  }

  wordList(list: string) {
    console.log("setting list to " + list);
    this.word_list_name = list;
    this.firstWordService.loadFirstWordList(list, this.sort_order).subscribe(response => this.checkResponse(response));
  }

  setSortOrder(sort_order: string): void {
    this.sort_order = sort_order;
    this.firstWordService.loadFirstWordList(this.word_list_name, this.sort_order).subscribe(response => this.checkResponse(response));
  } 

  checkWord() {
    console.log("first word is " + this.firstWord);
    if ( this.firstWord.length == 5 ) {
      console.log("Checking word...");
      this.firstWordService.loadFirstWordData(this.word_list_name, this.firstWord, this.sort_order).subscribe(response => this.checkDataRes(response));
      this.firstWord = '';
    }
  }

  checkDataRes(response: FirstWordResponse) {
    console.log("got word data\"" + response.res + '"');
    if ( response.res === "OK" ){
      console.log(response.words)
      this.added_word_list = this.added_word_list.concat(response.words);
      this.word_list = this.top_word_list.concat(this.added_word_list);
    } else {
      console.log("bad response from server \"" + response.res + "\"")
    }
  }

  checkResponse(response: FirstWordResponse) {
    console.log("got word list\"" + response.res + '"');
    if ( response.res === "OK" ){
      this.top_word_list = response.words;
      this.word_list = this.top_word_list.concat(this.added_word_list);
    } else {
      console.log("bad response from server \"" + response.res + "\"")
    }
  }
}
