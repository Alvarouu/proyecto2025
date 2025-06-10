import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { TokenService } from '../tokenStorage/token-service.service';
import * as Constant from '../../constant'
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AusenciaService {

  private registrarAusenciaUrl = Constant.baseUrl + 'registrar-ausencia/';
  private consultarAusenciaUrl =  Constant.baseUrl + 'consultar-ausencia/';
  private justificarAusenciaUrl =  Constant.baseUrl + 'justificar/';
  private enviarInformeAusencia = Constant.baseUrl + 'informe-ausencia/'
  constructor(private http: HttpClient, private tokenService: TokenService) {}

  registrarAusencia(ausencia: any) {
    const token = this.tokenService.getToken();
    const headers = new HttpHeaders({
      'Authorization': `Token ${token}`
    });

    return this.http.post(this.registrarAusenciaUrl, ausencia, { headers });
  }

  enviarInformeAusencias(): Observable<any> {
  return this.http.post(this.enviarInformeAusencia, {});
}

  traerAusencia(){

    return this.http.get(this.consultarAusenciaUrl);
  }

  justificar(id: number){
    let justi = {
      id: id,
      justificar:true
    }
    return this.http.post(this.justificarAusenciaUrl, justi);
  }

  noJustificar(id: number){
    let justi = {
      id: id,
      justificar:false
    }
    return this.http.post(this.justificarAusenciaUrl, justi);
  }

}
