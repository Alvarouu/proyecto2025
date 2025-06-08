import { Component } from '@angular/core';
import { AusenciaService } from '../../services/ausencia/ausencia.service';
import { CommonModule } from '@angular/common';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

@Component({
  selector: 'app-ver-ausencia',
  imports: [CommonModule],
  templateUrl: './ver-ausencia.component.html',
  styleUrl: './ver-ausencia.component.css'
})
export class VerAusenciaComponent {

  ausencia: any[] = [];
  hoy = new Date();
  constructor (private ausenciaService: AusenciaService){}

  ngOnInit(): void {
    
    this.hoy.setHours(0, 0, 0, 0);
    this.traerAusencia()
  }

  traerAusencia(){
    this.ausenciaService.traerAusencia().subscribe({
      next: (data:any)=>{
        this.ausencia = Array.isArray(data) ? data : [];
         this.ausencia = data.filter((ausencia: any) => {
          const fechaAusencia = new Date(ausencia.fecha);
          return fechaAusencia >= this.hoy; // Solo ausencias de hoy o futuro
        });
        console.log(this.ausencia)
      },
      error: (err) =>{
        console.error('Error al obtener la ausencia', err);
      }
    })
  }

  justificar(id: number): void{
    this.ausenciaService.justificar(id).subscribe({
      next:()=>{
        this.traerAusencia()
      },
      error:(err) => {
         console.error('Error', err);
      }
    })
  }

  noJustificar(id: number): void{
    this.ausenciaService.noJustificar(id).subscribe({
      next:()=>{
        this.traerAusencia()
      },
      error:(err) => {
         console.error('Error', err);
      }
    })
  }

  downloadPDF(): void {
    const tabla = document.getElementById('IdTable'); // Asegúrate de que el id coincida
    if (!tabla) return;
    const botones = tabla?.querySelectorAll('.columnaBotones')
    console.log(botones)
    botones?.forEach(b=>b.classList.add('hidden'))
    console.log(botones)
    html2canvas(tabla).then(canvas => {
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF();
      const imgProps = pdf.getImageProperties(imgData);
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

      pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
      pdf.save('ParteAusencias.pdf');
    });
    botones?.forEach(b=>b.classList.remove('hidden'))
  }

}
