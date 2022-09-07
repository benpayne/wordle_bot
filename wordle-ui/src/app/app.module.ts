import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TodaysAnswerComponent } from './todays-answer/todays-answer.component';
import { PlayWordleComponent } from './play-wordle/play-wordle.component';
import { FirstWordComponent } from './first-word/first-word.component';

@NgModule({
  declarations: [
    AppComponent,
    TodaysAnswerComponent,
    PlayWordleComponent,
    FirstWordComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
