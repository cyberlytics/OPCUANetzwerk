import { Component, Input, OnDestroy, SimpleChanges } from '@angular/core';
import { NbThemeService } from '@nebular/theme';

import { Electricity, ElectricityChart, ElectricityData } from '../../../@core/data/electricity';
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
  @Input() listData: AirQualityTableData;


  //NgOnChanges to detect changes in input data
  ngOnChanges(changes: SimpleChanges): void {
    if (changes.chartData) {
      this.chartData = changes.chartData.currentValue;
    }

    if (changes.listData) {
      this.listData = changes.listData.currentValue;
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
  }

  ngOnDestroy() {
    this.alive = false;
  }
}
