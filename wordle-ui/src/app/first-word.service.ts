import { Injectable } from '@angular/core';
import { HttpParams, HttpClient } from '@angular/common/http';
import { FirstWordResponse } from './row';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FirstWordService {

  private first_word_url = '/data/first_word/';

  constructor(private http: HttpClient) { }

  loadFirstWordList(list_name: string, sort: string): Observable<FirstWordResponse> {
    let url = this.first_word_url + list_name
    console.log("get url " + url);
    let params = new HttpParams();
    params = params.append('sort', sort);
    return this.http.get<FirstWordResponse>(url, {params: params});
  }

  loadFirstWordData(list_name: string, word: string, sort: string): Observable<FirstWordResponse> {
    let url = this.first_word_url + list_name + "/" + word
    console.log("get url " + url);
    let params = new HttpParams();
    params = params.append('sort', sort);
    return this.http.get<FirstWordResponse>(url, {params: params});
  }
}
