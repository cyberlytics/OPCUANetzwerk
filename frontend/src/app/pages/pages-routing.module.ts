import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';

import { PagesComponent } from './pages.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { NotFoundComponent } from './miscellaneous/not-found/not-found.component';
import { SensorNodeDashboardComponent } from './SensorNode/sensornode-dashboard.component';

const routes: Routes = [{
  path: '',
  component: PagesComponent,
  children: [
    {
      path: 'not-found',
      component: NotFoundComponent,
    }, 
    {
      path: 'iot-dashboard',
      component: DashboardComponent,
    },
    {
      path: ':id',
      component: SensorNodeDashboardComponent,
    },
  
  ]
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PagesRoutingModule {
}
