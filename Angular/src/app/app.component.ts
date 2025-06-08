import { Component } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { LoginService } from './services/login/login.service';
import { TokenService } from './services/tokenStorage/token-service.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { SocialLoginModule } from '@abacritt/angularx-social-login';



@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLink, FormsModule, CommonModule, SocialLoginModule, ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'Angular';

  constructor(private loginService: LoginService, private tokenService: TokenService, private router : Router) {}
   
  ngOnInit(){
    this.subscribeLogin()
  }
  
  isLoggedIn(): boolean {
    return this.tokenService.getToken() !== null;
  }

  isAdmin(): boolean {
    const user = sessionStorage.getItem('esAdmin');
    return this.tokenService.getAdmin()|| false
  }
  
  logout(){
    let idUser = this.tokenService.getUser()

    this.loginService.logout(idUser).subscribe({
      next: () => {
        this.tokenService.removeToken()
        this.tokenService.removeUser()

        this.router.navigateByUrl('/')
      }
    })

  }

  subscribeLogin(){

    this.tokenService.emiterLogIn.subscribe(()=>{
      this.isAdmin()
    })

  }

}
