import { TestBed } from '@angular/core/testing';

import { TodaysAnswerService } from './todays-answer.service';

describe('TodaysAnswerService', () => {
  let service: TodaysAnswerService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TodaysAnswerService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
