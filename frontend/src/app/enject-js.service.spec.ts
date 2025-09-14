import { TestBed } from '@angular/core/testing';

import { EnjectJsService } from './enject-js.service';

describe('EnjectJsService', () => {
  let service: EnjectJsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(EnjectJsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
