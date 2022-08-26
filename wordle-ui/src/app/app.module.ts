import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TodaysAnswerComponent } from './todays-answer/todays-answer.component';
import { PlayWordleComponent } from './play-wordle/play-wordle.component';

@NgModule({
  declarations: [
    AppComponent,
    TodaysAnswerComponent,
    PlayWordleComponent
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
