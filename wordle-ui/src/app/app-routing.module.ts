import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PlayWordleComponent } from './play-wordle/play-wordle.component';
import { TodaysAnswerComponent } from './todays-answer/todays-answer.component';
import { FirstWordComponent } from './first-word/first-word.component';

const routes: Routes = [
  { path: 'play', component: PlayWordleComponent },
  { path: 'today', component: TodaysAnswerComponent },
  { path: 'first', component: FirstWordComponent },
  { path: '', redirectTo: '/today', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
