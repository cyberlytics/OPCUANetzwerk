import { NgModule } from '@angular/core';
import {
  NbActionsModule,
  NbButtonModule,
  NbCardModule,
  NbTabsetModule,
  NbUserModule,
  NbRadioModule,
  NbSelectModule,
  NbListModule,
  NbIconModule,
} from '@nebular/theme';
import { NgxEchartsModule } from 'ngx-echarts';
import { ThemeModule } from '../../@theme/theme.module';
import { FormsModule } from '@angular/forms';
import { SensorNodeDashboardComponent } from './sensornode-dashboard.component';
import { LineChartComponent } from './lineChartComponent/lineChart.component';
import { TemperatureGaugeComponent } from './temperatureGauge/temperatureGauge.component';

const components = [
  SensorNodeDashboardComponent,
  LineChartComponent,
  TemperatureGaugeComponent
];

@NgModule({
  imports: [
    FormsModule,
    ThemeModule,
    NbCardModule,
    NbUserModule,
    NbButtonModule,
    NbTabsetModule,
    NbActionsModule,
    NbRadioModule,
    NbSelectModule,
    NbListModule,
    NbIconModule,
    NbButtonModule,
    NgxEchartsModule,
  ],
  declarations: [ ...components, TemperatureGaugeComponent ],
})
export class SensorNodeDashboardModule { }
