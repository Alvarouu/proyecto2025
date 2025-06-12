import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { TokenService } from '../tokenStorage/token-service.service';
import { Observable, throwError, catchError } from 'rxjs';
import * as Constant from '../../constant'

interface Horario {
  idHorario: number;
  fecha: string;
  franja: number;
  asignatura: string;
}

@Injectable({ 
  providedIn: 'root'
})
export class HorarioService {

  constructor(private http: HttpClient, private tokenService: TokenService) {}

  private horarioProfAdmin = Constant.baseUrl + 'api/horario-profesor/'
  private horarioUrl = Constant.baseUrl + 'horario/'
  private horarioProfUrl = Constant.baseUrl + 'horarios-profesor/'
  
  private getAuthHeaders() {
    const token = this.tokenService.getToken();
    return new HttpHeaders({
      'Authorization': `Token ${token}`
    });
  }
  
  
  getHorarioPorCorreo(correo: string): Observable<any[]> {
    const params = new HttpParams().set('correo', correo);

    return this.http.get<any[]>(this.horarioProfAdmin, { params }).pipe(
      catchError(err => {
        console.error('Error al obtener horario:', err);
        return throwError(() => new Error('No se pudo cargar el horario.'));
      })
    );
  }

  obtenerHorario() {
    const headers = this.getAuthHeaders();
    return this.http.get<any[]>(this.horarioUrl, { headers });
  }

getHorariosPorProfesor(idProfesor: number): Observable<Horario[]> {
  return this.http.get<Horario[]>(this.horarioProfUrl + `${idProfesor}/`);
}

}