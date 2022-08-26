import { TestBed } from '@angular/core/testing';

import { WordleGameService } from './wordle-game.service';

describe('WordleGameService', () => {
  let service: WordleGameService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(WordleGameService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
