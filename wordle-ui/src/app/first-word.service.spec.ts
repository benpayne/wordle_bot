import { TestBed } from '@angular/core/testing';

import { FirstWordService } from './first-word.service';

describe('FirstWordService', () => {
  let service: FirstWordService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FirstWordService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
