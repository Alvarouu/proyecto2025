import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VerAusenciaComponent } from './ver-ausencia.component';

describe('VerAusenciaComponent', () => {
  let component: VerAusenciaComponent;
  let fixture: ComponentFixture<VerAusenciaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [VerAusenciaComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(VerAusenciaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
