import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { TokenService } from '../services/tokenStorage/token-service.service';
import { tap } from 'rxjs';

@Component({
  selector: 'app-eliminar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './eliminarprofesores.component.html',
  styleUrls: ['./eliminarprofesores.component.css']
})
export class EliminarComponent implements OnInit {
  profesores: any[] = [];
  profesoresPaginados: any[] = [];
  paginaActual: number = 1;
  elementosPorPagina: number = 13;
  totalPaginas: number = 1;

  constructor(private http: HttpClient, private tokenService: TokenService) { }

  ngOnInit(): void {
    this.obtenerProfesores();
  }


  obtenerProfesores(): void {
    const token = this.tokenService.getToken();

    if (!token) {
      console.error('No se encontró el token');
      return;
    }

    const headers = new HttpHeaders({
      'Authorization': `Token ${token}`
    });

    this.http.get<any>('http://127.0.0.1:8000/profesores/', { headers }).subscribe({
      next: (data) => {
        console.log('Profesores obtenidos (RAW):', data);
        this.profesores = data;
        this.totalPaginas = Math.ceil(this.profesores.length / this.elementosPorPagina);
        this.actualizarProfesoresPaginados();
      },
      error: (error) => {
        console.error('Error obteniendo profesores', error);
      }
    });
  }

  eliminarProfesor(id: number): void {
    if (confirm('¿Estás seguro de que quieres eliminar este profesor?')) {
      const token = this.tokenService.getToken();

      const headers = new HttpHeaders({
        'Authorization': `Token ${token}`
      });

      this.http.delete(`http://127.0.0.1:8000/profesores/${id}/`, { headers }).subscribe({
        next: () => {
          alert('Profesor eliminado');
          this.obtenerProfesores();
        },
        error: (err) => {
          console.error('Error al eliminar', err);
        }
      });
    }
  }

  actualizarProfesoresPaginados() {
    const inicio = (this.paginaActual - 1) * this.elementosPorPagina;
    const fin = inicio + this.elementosPorPagina;
    this.profesoresPaginados = this.profesores.slice(inicio, fin);
  }

  cambiarPagina(nuevaPagina: number) {
    if (nuevaPagina >= 1 && nuevaPagina <= this.totalPaginas) {
      this.paginaActual = nuevaPagina;
      this.actualizarProfesoresPaginados();


    }
  }
}
