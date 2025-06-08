import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import * as Constant from '../../constant'

@Injectable({
  providedIn: 'root'
})
export class PerfilService {

  constructor(private http: HttpClient) { }

    private perfilUrl = Constant.baseUrl + 'perfil/'
    private cambiarContraseniaUrl = Constant.baseUrl + 'cambiar-contrasenia/'

    getPerfil(): Observable<any> {
      const token = localStorage.getItem('token');
      const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
      return this.http.get(this.perfilUrl, { headers });
    }

    cambiarContrasenia(nueva: string): Observable<any> {
      const token = localStorage.getItem('token');
      return this.http.post(
        this.cambiarContraseniaUrl,
        { nueva_contrasenia: nueva },
        { headers: { Authorization: `Bearer ${token}` } }
      );
    }

}