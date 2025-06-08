import { Component } from '@angular/core';
import { AusenciaService } from '../../services/ausencia/ausencia.service';
import { TokenService } from '../../services/tokenStorage/token-service.service';
import { HorarioService } from '../../services/horario/horario.service';
import { FormControl, Validators, FormGroup, FormsModule, ReactiveFormsModule} from '@angular/forms';
import { CommonModule } from '@angular/common';
import { request } from 'http';
import { Ausencia } from '../../models/Ausencia';


@Component({
  selector: 'app-ausencia',
  imports:[FormsModule, CommonModule, ReactiveFormsModule],
  templateUrl: './ausencia.component.html',
  styleUrls: ['./ausencia.component.css']
})
export class AusenciaComponent {
  comentario: string = '';
  fecha: string = '';
  horarios: any[] = [];
  idHorario: number = 0;

  constructor(private ausenciaService: AusenciaService, private tokenService: TokenService, private horarioService : HorarioService) {}

  newForm(): FormGroup{
    return new FormGroup({
      horario: new FormControl('', [Validators.required]),
      comentario: new FormControl('', []),
    })
  }

  form: FormGroup= this.newForm()

 ngOnInit() {
  const idProfesorString = this.tokenService.getUser();
  const idProfesor = idProfesorString ? parseInt(idProfesorString, 10) : null;

  if (idProfesor !== null && !isNaN(idProfesor)) {
    this.horarioService.getHorariosPorProfesor(idProfesor).subscribe({
      next: (res) => {
        const hoy = new Date();
        hoy.setHours(0, 0, 0, 0);  // Para comparar solo la fecha, sin la hora

        this.horarios = res.filter((horario: any) => {
          const partesFecha = horario.fecha.split('/');
          const fechaHorario = new Date(
            parseInt(partesFecha[2]),  // año
            parseInt(partesFecha[1]) - 1,  // mes (0-indexed)
            parseInt(partesFecha[0])  // día
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
      return;
    }
    let request:Ausencia={} as Ausencia
    request.idHorario = this.form.get('horario')?.value
    request.comentario = this.form.get('comentario')?.value
     console.log('Datos enviados:', request);

    this.ausenciaService.registrarAusencia(request).subscribe({
      next: (respuesta) => {
        alert('Ausencia registrada');
        console.log('Ausencia registrada:', respuesta);
      },
      error: (error) => {
        console.error('Error al registrar la ausencia:', error);
      }
    });
  }
}
