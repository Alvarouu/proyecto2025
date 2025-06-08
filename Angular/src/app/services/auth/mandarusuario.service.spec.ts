import { TestBed } from '@angular/core/testing';

import { MandarusuarioService } from './mandarusuario.service';

describe('MandarusuarioService', () => {
  let service: MandarusuarioService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MandarusuarioService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
