import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PlayWordleComponent } from './play-wordle/play-wordle.component';
import { TodaysAnswerComponent } from './todays-answer/todays-answer.component';

const routes: Routes = [
  { path: 'play', component: PlayWordleComponent },
  { path: 'today', component: TodaysAnswerComponent },
  { path: '', redirectTo: '/today', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
