import {Component, OnDestroy} from '@angular/core';
import { NbThemeService } from '@nebular/theme';
import { takeWhile } from 'rxjs/operators' ;
import { SolarData } from '../../@core/data/solar';
import {  LineChartDataSeries } from './lineChartComponent/LineChartDataClass';

interface CardSettings {
  title: string;
  iconClass: string;
  type: string;
}

@Component({
  selector: 'sensornode-dashboard',
  styleUrls: ['./sensornode-dashboard.component.scss'],
  templateUrl: './sensornode-dashboard.component.html',
})
export class SensorNodeDashboardComponent implements OnDestroy {

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

  ChartDataObj: LineChartDataSeries[] = [this.Series1, this.Series2];
  ChartDataObj2: LineChartDataSeries[] = [this.Series3, this.Series4];


  constructor(private theme: NbThemeService,) {
  }

  private alive = true;
  ngOnDestroy() {
    this.alive = false;
  }

  setChartData() {
    console.log("setChartData");
    this.ChartDataObj = this.ChartDataObj2;
  }
}
