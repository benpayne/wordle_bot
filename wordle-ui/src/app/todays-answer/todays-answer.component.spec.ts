import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TodaysAnswerComponent } from './todays-answer.component';

describe('TodaysAnswerComponent', () => {
  let component: TodaysAnswerComponent;
  let fixture: ComponentFixture<TodaysAnswerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TodaysAnswerComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TodaysAnswerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
