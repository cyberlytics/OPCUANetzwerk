import { Component, Input, OnDestroy, SimpleChanges } from '@angular/core';
import { NbThemeService } from '@nebular/theme';

import { Electricity, ElectricityChart, ElectricityData } from '../../../@core/data/electricity';
import { takeWhile } from 'rxjs/operators';
import { forkJoin } from 'rxjs';
import { LineChartDataSeries } from '../lineChartComponent/LineChartDataClass';
import { AirQualityData } from './AirQualityChart/air-quality-data';

const tmpData= [
  {
      "month": "Jan",
      "delta": "0.97",
      "down": true,
      "kWatts": "816",
      "cost": "97"
  },
  {
      "month": "Feb",
      "delta": "1.83",
      "down": true,
      "kWatts": "806",
      "cost": "95"
  },
  {
      "month": "Mar",
      "delta": "0.64",
      "down": true,
      "kWatts": "803",
      "cost": "94"
  },
  {
      "month": "Apr",
      "delta": "2.17",
      "down": false,
      "kWatts": "818",
      "cost": "98"
  },
  {
      "month": "May",
      "delta": "1.32",
      "down": true,
      "kWatts": "809",
      "cost": "96"
  },
  {
      "month": "Jun",
      "delta": "0.05",
      "down": true,
      "kWatts": "808",
      "cost": "96"
  },
  {
      "month": "Jul",
      "delta": "1.39",
      "down": false,
      "kWatts": "815",
      "cost": "97"
  },
  {
      "month": "Aug",
      "delta": "0.73",
      "down": true,
      "kWatts": "807",
      "cost": "95"
  },
  {
      "month": "Sept",
      "delta": "2.61",
      "down": true,
      "kWatts": "792",
      "cost": "92"
  },
  {
      "month": "Oct",
      "delta": "0.16",
      "down": true,
      "kWatts": "791",
      "cost": "92"
  },
  {
      "month": "Nov",
      "delta": "1.71",
      "down": true,
      "kWatts": "786",
      "cost": "89"
  },
  {
      "month": "Dec",
      "delta": "0.37",
      "down": false,
      "kWatts": "789",
      "cost": "91"
  }
]

const tmp2= [
  {
      "Date": "01.01.2020",
      "delta": "0.97",
      "down": true,
      "ppm": "816",
  },
  {
      "Date": "02.01.2020",
      "delta": "1.83",
      "down": true,
      "ppm": "806",
  },
  {
      "Date": "03.01.2020",
      "delta": "0.64",
      "down": true,
      "ppm": "803",
  },
  {
      "Date": "04.01.2020",
      "delta": "2.17",
      "down": false,
      "ppm": "818",
  },
  {
      "Date": "05.01.2020",
      "delta": "1.32",
      "down": true,
      "ppm": "809",
  },
  {
      "Date": "06.01.2020",
      "delta": "0.05",
      "down": true,
      "ppm": "808",
  },
  {
      "Date": "07.01.2020",
      "delta": "1.39",
      "down": false,
      "ppm": "815",
  },
  {
      "Date": "08.01.2020",
      "delta": "0.73",
      "down": true,
      "ppm": "807",
  },
  {
      "Date": "09.01.2020",
      "delta": "2.61",
      "down": true,
      "ppm": "792",
  },
  {
      "Date": "10.01.2020",
      "delta": "0.16",
      "down": true,
      "ppm": "791",
  },
  {
      "Date": "11.01.2020",
      "delta": "1.71",
      "down": true,
      "ppm": "786",
  },
  {
      "Date": "12.01.2020",
      "delta": "0.37",
      "down": false,
      "ppm": "789",
  }
]

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

  tmp = tmpData;
  tmp2 = tmp2;


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
        console.log("listData: ", listData); 
      });
  }

  ngOnDestroy() {
    this.alive = false;
  }
}
