import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HorarioService } from '../../services/horario/horario.service';

@Component({
  selector: 'app-ver-horario-profesor',
  templateUrl: './horario-admin.component.html',
  styleUrls: ['./horario-admin.component.css'],
  standalone: true,
  imports: [CommonModule, FormsModule]
})
export class VerHorarioProfesorComponent {
  correo: string = '';
  horario: any[] = [];
  loading = false;
  error = '';

  constructor(private horarioService: HorarioService) {}

  buscarHorario() {
    this.loading = true;
    this.error = '';
    this.horario = [];

    if (!this.correo || !this.correo.includes('@')) {
      this.error = 'Debes introducir un correo válido.';
      this.loading = false;
      return;
    }

    this.horarioService.getHorarioPorCorreo(this.correo).subscribe({
      next: (data) => {
        this.horario = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'No se encontró el horario del profesor.';
        this.loading = false;
      }
    });
  }
}