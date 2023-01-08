import { Component, Input, OnDestroy, SimpleChanges } from '@angular/core';
import { NbThemeService } from '@nebular/theme';

import { takeWhile } from 'rxjs/operators';
import { forkJoin } from 'rxjs';
import { LineChartDataSeries } from '../lineChartComponent/LineChartDataClass';
import { AirQualityData } from './AirQualityChart/air-quality-data';
import { AirQualityTableData } from './air-quality-list-data';


@Component({
  selector: 'air-quality',
  styleUrls: ['./air-quality.component.scss'],
  templateUrl: './air-quality.component.html',
})
export class AirQualityComponent implements OnDestroy {

  private alive = true;
  
  @Input() chartData: AirQualityData;
  @Input() listData: AirQualityTableData[];


  //NgOnChanges to detect changes in input data
  ngOnChanges(changes: SimpleChanges): void {
    if (changes.chartData) {
      //round the values to 2 decimal places
      this.chartData = this.roundChartDataValues(changes.chartData.currentValue);
    }

    if (changes.listData) {
      this.listData = this.roundListDataValues(changes.listData.currentValue);
    }
  }
    

  currentTheme: string;
  themeSubscription: any;

  constructor(private themeService: NbThemeService) {
    this.themeService.getJsTheme()
      .pipe(takeWhile(() => this.alive))
      .subscribe(theme => {
        this.currentTheme = theme.name;
    });
  }

  ngOnDestroy() {
    this.alive = false;
  }

  roundChartDataValues(chartData: AirQualityData): AirQualityData {
    chartData.data.forEach((dataPoint) => {
      dataPoint[1] = Math.round(dataPoint[1] * 100) / 100;
    });
    return chartData;
  }

  roundListDataValues(listData: AirQualityTableData[]): AirQualityTableData[] {
    listData.forEach((dataPoint) => {
      var avg = +dataPoint.average
      var delta = +dataPoint.delta
      dataPoint.average = (Math.round(avg * 100) / 100).toString();
      dataPoint.delta = (Math.round(delta * 100) / 100).toString();
    });
    return listData;
  }
    
}
