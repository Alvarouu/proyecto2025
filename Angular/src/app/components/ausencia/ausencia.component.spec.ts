import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AusenciaComponent } from './ausencia.component';

describe('AusenciaComponent', () => {
  let component: AusenciaComponent;
  let fixture: ComponentFixture<AusenciaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AusenciaComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AusenciaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
