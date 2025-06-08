import { TestBed } from '@angular/core/testing';

import { AusenciaService } from './ausencia.service';

describe('AusenciaService', () => {
  let service: AusenciaService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AusenciaService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
