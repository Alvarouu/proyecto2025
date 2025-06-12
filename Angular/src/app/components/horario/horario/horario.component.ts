import { Component, OnInit } from '@angular/core';
import { HorarioService } from '../../../services/horario/horario.service';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import * as Constant from '../../../constant'

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
  private verSeman = Constant.baseUrl + 'horario/semana/'
  private onCursoChang = Constant.baseUrl + 'horario/curso/'
  private onAulaChang = Constant.baseUrl + 'horario/aula/'
  private cargarCurso = Constant.baseUrl + 'horario/cursos/'
  private cargarAula = Constant.baseUrl + 'horario/aulas/'
  private verhoy = Constant.baseUrl + 'horario/hoy/'
  


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
    this.http.get<any[]>(this.verSeman).subscribe({
      next: (data: any[]) => {
        this.horario = Array.isArray(data) ? data : [];
      },
      error: (error: any) => {
        console.error('Error al obtener clases de la semana', error);
      }
    });
    }

    verHoy(): void {
    this.http.get<any[]>(this.verhoy).subscribe({
      next: (data: any[]) => {
        this.horario = Array.isArray(data) ? data : [];
      },
      error: (error: any) => {
        console.error('Error al obtener clases de verHoy', error);
      }
    });
    }

  onCursoChange(): void {
    if (this.selectedCursoId) {
      this.http.get<any[]>(this.onCursoChang + `${this.selectedCursoId}/`).subscribe({
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
      this.http.get<any[]>(this.onAulaChang + `${this.selectedAulaId}/`).subscribe({
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
    this.http.get<any[]>(this.cargarCurso).subscribe({
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
    this.http.get<any[]>(this.cargarAula).subscribe({
      next: (data: any[]) => {
        this.aulas = data;
      },
      error: (err) => {
        console.error('Error al cargar aulas:', err);
      }
    });
  }
    
  }