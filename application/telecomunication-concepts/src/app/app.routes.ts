import { Routes } from '@angular/router';
import { NotFoundError } from '@angular/core/primitives/di';
import { Home } from './components/home/home.component';

export const routes: Routes = [
    {path:'', component: Home},
    {path:'**', component:NotFoundError}
];
