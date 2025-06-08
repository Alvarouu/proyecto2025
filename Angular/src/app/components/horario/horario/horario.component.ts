import { Component, OnInit } from '@angular/core';
import { HorarioService } from '../../../services/horario/horario.service';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-horario',
  templateUrl: './horario.component.html',
  imports: [CommonModule, FormsModule],
  styleUrls: ['./horario.component.css']
})
export class HorarioComponent implements OnInit {
  horario: any[] = [];
  horarios: any[] = [];
  clasesSemana: any[] = [];
  cursos: any[] = [];
  aulas: any[] = [];
  selectedCursoId: number | null = null;
  selectedAulaId: number | null = null;
  constructor(private horarioService: HorarioService, private http: HttpClient) {}

  ngOnInit(): void {
    this.cargarCursos();
    this.cargarAulas();
    this.horarioService.obtenerHorario().subscribe({
      next: (data: any) => {
        this.horario = Array.isArray(data) ? data : [];
      },
      error: (err) => {
        console.error('Error al obtener el horario:', err);
      }
    });

  }
  
  verSemana(): void {
    this.http.get<any[]>('http://127.0.0.1:8000/horario/semana/').subscribe({
      next: (data: any[]) => {
        this.horario = Array.isArray(data) ? data : [];
      },
      error: (error: any) => {
        console.error('Error al obtener clases de la semana', error);
      }
    });
    }

  onCursoChange(): void {
    if (this.selectedCursoId) {
      this.http.get<any[]>(`http://127.0.0.1:8000/horario/curso/${this.selectedCursoId}/`).subscribe({
        next: (data: any[]) => {
          this.horario = Array.isArray(data) ? data : [];
        },
        error: (error) => {
          console.error(`Error al obtener horarios del curso con ID ${this.selectedCursoId}:`, error);
        }
      });
    }
  }

  // Filtrar por aula seleccionada
  onAulaChange(): void {
    if (this.selectedAulaId) {
      this.http.get<any[]>(`http://127.0.0.1:8000/horario/aula/${this.selectedAulaId}/`).subscribe({
        next: (data: any[]) => {
          this.horario = Array.isArray(data) ? data : [];
        },
        error: (error) => {
          console.error(`Error al obtener horarios del aula con ID ${this.selectedAulaId}:`, error);
        }
      });
    }
  }

  // Cargar lista de cursos desde backend
  cargarCursos(): void {
    this.http.get<any[]>('http://127.0.0.1:8000/horario/cursos/').subscribe({
      next: (data: any[]) => {
        this.cursos = data;
      },
      error: (err) => {
        console.error('Error al cargar cursos:', err);
      }
    });
  }

  // Cargar lista de aulas desde backend
  cargarAulas(): void {
    this.http.get<any[]>('http://127.0.0.1:8000/horario/aulas/').subscribe({
      next: (data: any[]) => {
        this.aulas = data;
      },
      error: (err) => {
        console.error('Error al cargar aulas:', err);
      }
    });
  }
    
  }