import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Router } from '@angular/router';
import * as Constant from '../../constant'

@Injectable({
  providedIn: 'root'
})
export class LoginService {
  private loginURL = Constant.baseUrl + 'login/';
  private logoutURL = Constant.baseUrl + 'logout/'
  private loginGoogleURL = Constant.baseUrl + 'loginG/'

  constructor(private http: HttpClient, private router: Router) {}

  loginUser(credentials: { correo: string, contrasenia: string }): Observable<any> {
    const payload = {
      correo: credentials.correo,
      password: credentials.contrasenia
    };
  
    return this.http.post(this.loginURL, payload);
  }

    loginG(token:string ): Observable<any> {
    const payload = {
      token:token,
      type:'google'
    };
  
    return this.http.post(this.loginGoogleURL, payload);
  }

  logout(idUser: any){

    return this.http.get(this.logoutURL+idUser)

  }

}
