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

  constructor(private firstWordService: FirstWordService) { }

  ngOnInit(): void {
    this.firstWordService.loadFirstWordList('all').subscribe(response => this.checkResponse(response));
  }

  checkResponse(response: FirstWordResponse)
  {
    console.log("got word list\"" + response.res + '"');
    if ( response.res === "OK" ){
      this.word_list = response.words;
    } else {
      console.log("bad response from server \"" + response.res + "\"")
    }
  }
}
