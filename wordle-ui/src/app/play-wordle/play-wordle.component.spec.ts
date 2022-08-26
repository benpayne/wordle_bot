import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlayWordleComponent } from './play-wordle.component';

describe('PlayWordleComponent', () => {
  let component: PlayWordleComponent;
  let fixture: ComponentFixture<PlayWordleComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PlayWordleComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PlayWordleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
