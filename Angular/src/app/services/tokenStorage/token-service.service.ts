import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TokenService {
  
  public emiterLogIn: Subject<boolean> = new Subject<boolean>()
  private TOKEN_KEY = 'accessToken';
  private USER_KEY = 'idUser'
  private USER_ADMIN =  'admin'

  constructor() {}

  // Verifica si el entorno es cliente antes de acceder a sessionStorage
  private isClient() {
    return typeof window !== 'undefined' && window.sessionStorage;
  }

  // Almacena token securely
  public setToken(token: string): void {
    if (this.isClient()) {
      sessionStorage.setItem(this.TOKEN_KEY, token);
    }
  }

  // Trae token
  public getToken(): string | null {
    if (this.isClient()) {
      return sessionStorage.getItem(this.TOKEN_KEY);
    }
    return null;
  }

  // Elimina token
  public removeToken(): void {
    if (this.isClient()) {
      sessionStorage.removeItem(this.TOKEN_KEY);
    }
  }

  // Almacena user id
  public setUser(idUser: any): void {
    if (this.isClient()) {
      sessionStorage.setItem(this.USER_KEY, idUser);
    }
  }

  // Trae user id
  public getUser(): string | null {
    if (this.isClient()) {
      return sessionStorage.getItem(this.USER_KEY);
    }
    return null;
  }

  // Elimina user id
  public removeUser(): void {
    if (this.isClient()) {
      sessionStorage.removeItem(this.USER_KEY);
    }
  }

  // Trae prof admin
  public getAdmin(): boolean | null {
    if (this.isClient()) {
      return sessionStorage.getItem(this.USER_ADMIN)?.toLowerCase() == 'true';
    }
    return null;
  }

  // Elimina prof admin
  public removeAdmin(): void {
    if (this.isClient()) {
      sessionStorage.removeItem(this.USER_ADMIN);
    }
  }
  
  // Almacena prof admin
  public setAdmin(admin: Boolean): void {
    if (this.isClient()) {
      sessionStorage.setItem(this.USER_ADMIN, String(admin));
    }
  }

}
