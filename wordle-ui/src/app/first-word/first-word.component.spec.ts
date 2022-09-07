import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FirstWordComponent } from './first-word.component';

describe('FirstWordComponent', () => {
  let component: FirstWordComponent;
  let fixture: ComponentFixture<FirstWordComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FirstWordComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FirstWordComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
