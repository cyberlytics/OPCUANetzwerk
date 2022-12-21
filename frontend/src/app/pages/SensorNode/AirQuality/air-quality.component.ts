import { Component, Input, OnDestroy, SimpleChanges } from '@angular/core';
import { NbThemeService } from '@nebular/theme';

import { Electricity, ElectricityChart, ElectricityData } from '../../../@core/data/electricity';
import { takeWhile } from 'rxjs/operators';
import { forkJoin } from 'rxjs';
import { LineChartDataSeries } from '../lineChartComponent/LineChartDataClass';
import { AirQualityData } from './AirQualityChart/air-quality-data';

@Component({
  selector: 'air-quality',
  styleUrls: ['./air-quality.component.scss'],
  templateUrl: './air-quality.component.html',
})
export class AirQualityComponent implements OnDestroy {

  private alive = true;

  listData: Electricity[];
  //input for chart data
  
  @Input() chartData: AirQualityData;

  type = 'week';
  types = ['week', 'month', 'year'];

   Temperature: AirQualityData = {
    data: [["2018-08-15T10:04:01.339Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-16T10:14:13.914Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-17T10:04:01.339Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-18T10:14:13.914Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-19T10:04:01.339Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-20T10:14:13.914Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-21T10:04:01.339Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-22T10:14:13.914Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-23T10:04:01.339Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-24T10:14:13.914Z",Math.round(Math.random()* 100* 100) / 100]],
  }

  //NgOnChanges to detect changes in input data
  ngOnChanges(changes: SimpleChanges): void {
    if (changes.chartData) {
      this.chartData = changes.chartData.currentValue;
    }
  }
    

  currentTheme: string;
  themeSubscription: any;

  constructor(private electricityService: ElectricityData,
              private themeService: NbThemeService) {
    this.themeService.getJsTheme()
      .pipe(takeWhile(() => this.alive))
      .subscribe(theme => {
        this.currentTheme = theme.name;
    });

    forkJoin(
      this.electricityService.getListData(),
      this.electricityService.getChartData(),
    )
      .pipe(takeWhile(() => this.alive))
      .subscribe(([listData, chartData]: [Electricity[], ElectricityChart[]] ) => {
        this.listData = listData;
      });
  }

  ngOnDestroy() {
    this.alive = false;
  }
}
