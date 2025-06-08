import { Component, OnInit } from '@angular/core';
import { PerfilService } from '../../../services/perfil/perfil.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-perfil',
  imports:[CommonModule, FormsModule],
  templateUrl: './perfil.component.html',
  styleUrls: ['./perfil.component.css']
})
export class PerfilComponent implements OnInit {

  usuario: any; // Aquí se guardará la información del perfil
  mostrarFormulario = false;
  nuevaContrasenia = '';
  constructor(private perfilService: PerfilService) {}

  ngOnInit() {
    this.perfilService.getPerfil().subscribe({
      next: data => this.usuario = data,
      error: err => console.error('Error obteniendo perfil:', err)
    });
  }

  cambiarContrasenia() {
    if (!this.nuevaContrasenia) {
      alert('Introduce una nueva contraseña');
      return;
    }

    this.perfilService.cambiarContrasenia(this.nuevaContrasenia).subscribe({
      next: () => {
        alert('Contraseña actualizada correctamente');
        this.nuevaContrasenia = '';
        this.mostrarFormulario = false;
      },
      error: err => {
        console.error('Error al cambiar la contraseña', err);
        alert('Hubo un error al cambiar la contraseña');
      }
    });
  }

}