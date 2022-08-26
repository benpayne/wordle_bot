import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { WordleRow, LetterState, TodaysAnswerResponse } from './row';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TodaysAnswerService {

  private word_list_url = '/data/';

  constructor(private http: HttpClient) {
  }

  loadRows(): Observable<TodaysAnswerResponse> {
    let yourDate = new Date()
    let url = this.word_list_url + yourDate.getFullYear() + "-" + 
      String(yourDate.getMonth() + 1).padStart(2, "0") + "-" + 
      String(yourDate.getDate()).padStart(2, "0")
    console.log("get url " + url);
    return this.http.get<TodaysAnswerResponse>(url);
  }
}
