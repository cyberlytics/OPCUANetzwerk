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
import { SwitchComponent } from './switch/switch.component';
import { GanttComponent } from './gantt/gantt.component';
import { TemoSensorCardComponent } from './tempSensorCard/tempSensorCard.component';
import { BackendDataService } from '../../Services/BackendDataService';

const components = [
  SensorNodeDashboardComponent,
  LineChartComponent,
  TemperatureGaugeComponent,
  SwitchComponent,
  GanttComponent,
  TemoSensorCardComponent,
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
  declarations: [ ...components, TemperatureGaugeComponent, SwitchComponent, GanttComponent ],
  providers: [BackendDataService],
})
export class SensorNodeDashboardModule { }
