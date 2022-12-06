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

  ngOnChanges(changes: SimpleChanges): void {}

  flipped = false;

  ngAfterViewInit() {

    console.log("temperature input: ", this.Temperature)

    this.ChartDataObj = [this.Temperature, this.Humidity, this.AirPresure]

    this.GaugeTemperature = this.Temperature.data[this.Temperature.data.length-1][1]
    this.GaugeHumidity = this.Humidity.data[this.Humidity.data.length-1][1]
    this.GaugeAirPresure = this.AirPresure.data[this.AirPresure.data.length-1][1]
    
    //printe GaugeTemperature, GaugeHumidity, GaugeAirPresure
    console.log("GaugeTemperature: ", this.GaugeTemperature)
    console.log("GaugeHumidity: ", this.GaugeHumidity)
    console.log("GaugeAirPresure: ", this.GaugeAirPresure)
  }

  Series1: LineChartDataSeries = {
    name: "Series1",
    type: "line",
    data: [["2018-08-15T10:04:01.339Z",5],["2018-08-15T10:14:13.914Z",7]]
  }

  Series2: LineChartDataSeries = {
    name: "Series2",
    type: "line",
    data: [["2018-08-15T10:04:01.339Z",10],["2018-08-15T10:14:13.914Z",15]]
  }


  Series3: LineChartDataSeries = {
    name: "Series3",
    type: "line",
    data: [["2018-08-16T10:04:01.339Z",23],["2018-08-16T10:14:13.914Z",2]]
  }

  Series4: LineChartDataSeries = {
    name: "Series4",
    type: "line",
    data: [["2018-08-16T10:04:01.339Z",20],["2018-08-16T10:14:13.914Z",10]]
  }



  //Start Temperatur
  random = +(Math.random() * 60).toFixed(2);

  toggleView() {
    this.flipped = !this.flipped;
  }

  private alive = true;
  ngOnDestroy() {
    this.alive = false;
  }
}
