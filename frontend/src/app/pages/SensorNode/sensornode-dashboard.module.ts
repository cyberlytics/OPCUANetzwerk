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
  NbTimepickerModule,
  NbDatepickerModule,
  NbInputModule,
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
import { TimespanService } from '../../Services/TimespanProviderService';
import { LcdInputComponent } from './lcd-input/lcd-input.component';
import { AirQualityChartComponent } from './AirQuality/AirQualityChart/air-quality-chart.component';
import { AirQualityComponent } from './AirQuality/air-quality.component';
import { BuzzerFrequencyComponent } from './buzzerFrequency/buzzer-frequency/buzzer-frequency.component';

const components = [
  SensorNodeDashboardComponent,
  LineChartComponent,
  TemperatureGaugeComponent,
  SwitchComponent,
  GanttComponent,
  TemoSensorCardComponent,
  AirQualityChartComponent,
  AirQualityComponent
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
    NbInputModule
  ],
  declarations: [ ...components, TemperatureGaugeComponent, SwitchComponent, GanttComponent, LcdInputComponent, BuzzerFrequencyComponent ],
  providers: [BackendDataService, TimespanService],
})
export class SensorNodeDashboardModule { }
