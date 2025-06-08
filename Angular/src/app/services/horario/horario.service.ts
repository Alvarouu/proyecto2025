import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { TokenService } from '../tokenStorage/token-service.service';
import { Observable } from 'rxjs';
import * as Constant from '../../constant'

@Injectable({
  providedIn: 'root'
})
export class HorarioService {

  constructor(private http: HttpClient, private tokenService: TokenService) {}

  private horarioUrl = Constant.baseUrl + 'horario/'
  private horarioProfUrl = Constant.baseUrl + 'horarios-profesor/'

  private getAuthHeaders() {
    const token = this.tokenService.getToken();
    return new HttpHeaders({
      'Authorization': `Token ${token}`
    });
  }

  obtenerHorario() {
    const headers = this.getAuthHeaders();
    return this.http.get<any[]>(this.horarioUrl, { headers });
  }

  getHorariosPorProfesor(idProfesor: number): Observable<any[]> {
    return this.http.get<any[]>(this.horarioProfUrl + `${idProfesor}/`);
  }

}