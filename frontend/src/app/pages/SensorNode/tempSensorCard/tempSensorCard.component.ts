import {ChangeDetectionStrategy, Component, Input, OnChanges, OnDestroy, SimpleChanges} from '@angular/core';
import { NbThemeService } from '@nebular/theme';
import { takeWhile } from 'rxjs/operators' ;
import { SolarData } from '../../../@core/data/solar';
import {echarts} from 'echarts';
import { EChartsOption } from 'echarts';
import * as moment from 'moment';
import { LineChartDataSeries } from '../lineChartComponent/LineChartDataClass';

@Component({
  selector: 'tempSensorCard',
  styleUrls: ['./tempSensorCard.component.scss'],
  templateUrl: './tempSensorCard.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TemoSensorCardComponent implements OnDestroy, OnChanges {

  //inputs for temperature humidity and air presure
  @Input() Temperature: LineChartDataSeries;
  @Input() Humidity: LineChartDataSeries;
  @Input() AirPresure: LineChartDataSeries;

  GaugeTemperature: number
  GaugeHumidity: number
  GaugeAirPresure: number

  ChartDataObj: LineChartDataSeries[] 

  constructor(private theme: NbThemeService,) {
  }

  ngOnChanges(changes: SimpleChanges): void {
    this.Temperature = changes.Temperature.currentValue;
    this.Humidity = changes.Humidity.currentValue;
    this.AirPresure= changes.AirPresure.currentValue;

    this.refreshBoundObjects();
  }

  flipped = false;

  ngAfterViewInit() {
    this.refreshBoundObjects();
  }

  refreshBoundObjects(){
    //LineChart
    this.ChartDataObj = [this.Temperature, this.Humidity, this.AirPresure]

    //Gauges
    //onyl do this when the .data is not eqal to []
    if(this.Temperature.data.length == 0 || this.Humidity.data.length == 0 || this.AirPresure.data.length == 0){
      return;
    }

    this.GaugeTemperature = this.Temperature.data[this.Temperature.data.length-1][1]
    this.GaugeHumidity = this.Humidity.data[this.Humidity.data.length-1][1]
    this.GaugeAirPresure = this.AirPresure.data[this.AirPresure.data.length-1][1]
  }

  toggleView() {
    this.flipped = !this.flipped;
  }

  private alive = true;
  ngOnDestroy() {
    this.alive = false;
  }
}
