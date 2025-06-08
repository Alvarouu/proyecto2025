import { Component, NgZone } from '@angular/core';
import { LoginService } from '../../services/login/login.service';
import { FormsModule } from '@angular/forms';
import { TokenService } from '../../services/tokenStorage/token-service.service';
import { Router } from '@angular/router';
import { SocialAuthService, GoogleLoginProvider, SocialUser } from '@abacritt/angularx-social-login';

declare const google: any;
@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule,],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  correo: string = '';
  contrasenia: string = '';

  constructor(
    private loginService: LoginService,
    private tokenService: TokenService,
    private router: Router,
    private authService: SocialAuthService,
    private ngZone: NgZone,
  ) { }

  ngOnInit() {
    console.log("LoginComponent cargado");
    if (typeof window !== 'undefined') {
      window.onload = () => {
        google.accounts.id.initialize({
          client_id: '92500515360-q854c10je9ak7o0e9tsl02d6531crjrg.apps.googleusercontent.com',
          callback: (response: any) => this.onLoginGoogle(response),
        });

        google.accounts.id.renderButton(
          document.getElementById("google-btn"),
          { theme: "outline", size: "large" }
        );
      };

    }
  }

  onLogin() {
    const credenciales = {
      correo: this.correo,
      contrasenia: this.contrasenia
    };

    this.tokenService.removeToken();
    this.tokenService.removeUser();

    this.loginService.loginUser(credenciales).subscribe({
      next: (res) => {
        console.log("Login exitoso:", res.token);
        this.tokenService.setToken(res.token);
        this.tokenService.setUser(res.user);
        this.tokenService.setAdmin(res.admin);
        this.tokenService.emiterLogIn.next(true)

        alert('Login correcto!');
        this.router.navigate(['/horario']);
      },
      error: (err) => {
        console.error('Error en login', err);
        alert('Login incorrecto');
      }
    });
  }

  onLoginGoogle(response: any) {
    const credential = response.credential;
    this.tokenService.removeToken();
    this.tokenService.removeUser();

    this.loginService.loginG(credential).subscribe({
      next: (res) => {
        console.log("Login exitoso:", res.token);
        this.tokenService.setToken(res.token);
        this.tokenService.setUser(res.user);
        this.tokenService.setAdmin(res.admin);
        this.tokenService.emiterLogIn.next(true)

        alert('Login correcto!');
        this.router.navigate(['/horario']);
      },
      error: (err) => {
        console.error('Error en login', err);
        alert('Login incorrecto');
      }
    });
  }

}