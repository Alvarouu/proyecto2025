import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError, Observable, tap, throwError } from 'rxjs';
import * as Constant from '../../constant'
@Injectable({
  providedIn: 'root'
})
export class MandarusuarioService {

  userObj = {

    nombre : '',
    apellido1 : '',
    apellido2 : '',
    contrasenia: '',
    confirmarContrasenia: '',
    correo: '',
    esAdmin: false,
  }
  
  private apiURL = Constant.baseUrl + 'registro/register/';

  constructor(private http: HttpClient) { }

  register(userObj: any): Observable<any> {
    const payload = {
      nombre: userObj.nombre,
      apellido1: userObj.apellido1,
      apellido2: userObj.apellido2,
      correo: userObj.correo,
      password: userObj.contrasenia,
      esAdmin: userObj.esAdmin
    };
  
    return this.http.post(this.apiURL, payload).pipe(
      tap((response: any) => {
        alert("Funciona");
      }),
      catchError((error: any) => {
        console.error("Error en el registro", error);
        return throwError(() => error);
      })
    );
  }


}


