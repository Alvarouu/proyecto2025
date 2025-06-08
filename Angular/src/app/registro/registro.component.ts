import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms';
import { MandarusuarioService } from '../services/auth/mandarusuario.service';

@Component({
  selector: 'app-registro',
  imports: [FormsModule, CommonModule, ],
  templateUrl: './registro.component.html',
  styleUrl: './registro.component.css'
})

export class RegistroComponent {

  constructor(private servicio:MandarusuarioService){}

  userObj: any = {

    nombre : '',
    apellido1 : '',
    apellido2 : '',
    password: '',
    confirmarContrasenia: '',
    correo: '',
    esAdmin: false,
  }

  onSave() {
    const formValue = this.rellenar(this.userObj);
    this.servicio.register(formValue).subscribe({
      next: (res) => {
        alert('Usuario creado correctamente');
      },
      error: (err) => {
        alert('Error al registrar el usuario');
        console.error(err);
      }
    });
  }

rellenar(userObj: any) {
  const normalizar = (texto: string) =>
    texto
      .normalize('NFD')                  // Separa letras de acentos (e.g., é → e + ́)
      .replace(/[\u0300-\u036f]/g, '')   // Elimina los signos diacríticos (acentos)
      .replace(/\s+/g, '')               // Elimina espacios

  const nombre = normalizar(userObj.nombre);
  const apellido1 = normalizar(userObj.apellido1);

  userObj.correo = `${nombre}${apellido1}@iespoligonosur.org`.toLowerCase();
  return userObj;
}





}

