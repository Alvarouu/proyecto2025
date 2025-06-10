import { Component } from '@angular/core';
import { AusenciaService } from '../../services/ausencia/ausencia.service';
import { TokenService } from '../../services/tokenStorage/token-service.service';
import { HorarioService } from '../../services/horario/horario.service';
import { FormControl, FormGroup, Validators, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-ausencia',
  templateUrl: './ausencia.component.html',
  styleUrls: ['./ausencia.component.css'],
  standalone: true,
  imports: [FormsModule, ReactiveFormsModule, CommonModule]
})
export class AusenciaComponent {
  comentario: string = '';
  horarios: any[] = [];
  idHorario: number = 0;

  form: FormGroup = new FormGroup({
    horario: new FormControl('', [Validators.required]),
    comentario: new FormControl('')
  });

  constructor(
    private tokenService: TokenService,
    private ausenciaService: AusenciaService,
    private horarioService: HorarioService
  ) {}

  ngOnInit() {
    const idProfesorString = this.tokenService.getUser();
    const idProfesor = idProfesorString ? parseInt(idProfesorString, 10) : null;

    if (idProfesor !== null && !isNaN(idProfesor)) {
      this.horarioService.getHorariosPorProfesor(idProfesor).subscribe({
        next: (res) => {
          const hoy = new Date();
          hoy.setHours(0, 0, 0, 0);

          // Asegúrate de que cada horario tenga `idHorario` y `fecha`
          this.horarios = res.filter((horario: any) => {
            if (!horario.fecha) return false;

            const partesFecha = horario.fecha.split('/');
            if (partesFecha.length < 3) return false;

            const fechaHorario = new Date(
              parseInt(partesFecha[2]), 
              parseInt(partesFecha[1]) - 1, 
              parseInt(partesFecha[0])
            );
            return fechaHorario >= hoy;
          });
        },
        error: (err) => {
          console.error('Error al obtener horarios:', err);
        }
      });
    } else {
      console.error('ID de profesor no válido o no encontrado en el token');
    }
  }

  registrarAusencia() {
    const token = this.tokenService.getToken();
    if (!token) {
      console.error('Token no encontrado. El usuario no está autenticado.');
      alert('⚠️ No estás autenticado. Por favor, inicia sesión.');
      return;
    }

    const valorSeleccionado = this.form.get('horario')?.value;

    if (!valorSeleccionado || isNaN(valorSeleccionado)) {
      alert('❌ Debes seleccionar un horario válido.');
      return;
    }

    const idHorario = Number(valorSeleccionado);

    const request = {
      idHorario: idHorario,
      comentario: this.form.get('comentario')?.value || ''
    };

    console.log('Datos enviados:', request);

    this.ausenciaService.registrarAusencia(request).subscribe({
      next: (respuesta) => {
        alert('✅ Ausencia registrada correctamente');
        console.log('Ausencia registrada:', respuesta);
      },
      error: (error) => {
        console.error('❌ Error al registrar la ausencia:', error);
        alert(`🚫 Hubo un error al registrar la ausencia: ${error.statusText}`);
      }
    });
  }
}