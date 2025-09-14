import { TestBed } from '@angular/core/testing';

import { AlreadyAuthServiceService } from './already-auth-service.service';

describe('AlreadyAuthServiceService', () => {
  let service: AlreadyAuthServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AlreadyAuthServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
