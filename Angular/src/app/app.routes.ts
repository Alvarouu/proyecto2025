import { Routes } from '@angular/router';
import { RegistroComponent } from './registro/registro.component';
import { GetApiComponent } from './API/get-api/get-api.component';
import { LoginComponent } from './components/login/login.component';
import { LayoutComponent } from './layout/layout/layout.component';
import { EliminarComponent } from './eliminarprofesores/eliminarprofesores.component';
import { HorarioComponent } from './components/horario/horario/horario.component';
import { PerfilComponent } from './components/perfil/perfil/perfil.component';
import { AusenciaComponent } from './components/ausencia/ausencia.component';
import { VerAusenciaComponent } from './components/ver-ausencia/ver-ausencia.component';
import {VerHorarioProfesorComponent} from './components/horario-admin/horario-admin.component'

export const routes: Routes = [
    {
        path: '',
        redirectTo: 'login',
        pathMatch: 'full'
    },

    {
        path: 'login',
        component: LoginComponent
    },
    {
        path: 'layout',
        component: LayoutComponent,
    },
    {
        path: 'registro',
        component: RegistroComponent
    },

    {
        path: 'get-api',
        component: GetApiComponent
    },
    {
        path: 'eliminar-profesores',
        component: EliminarComponent
    },
    {
        path: 'horario',
        component: HorarioComponent
    },
    {
        path: 'perfil',
        component: PerfilComponent
    },
    {
        path: 'ausencia',
        component: AusenciaComponent
    },
    {
        path: 'consultaAusencia',
        component: VerAusenciaComponent
    },
        {
        path: 'verHorariosCompleto',
        component: VerHorarioProfesorComponent
    },
];
