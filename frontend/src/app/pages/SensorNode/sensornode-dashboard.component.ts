import {Component, OnDestroy} from '@angular/core';
import { NbThemeService } from '@nebular/theme';
import { takeWhile } from 'rxjs/operators' ;
import { SolarData } from '../../@core/data/solar';
import {  LineChartDataSeries } from './lineChartComponent/LineChartDataClass';
import {TemperatureGaugeDataSeries} from './temperatureGauge/temperatureGaugeData'

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


  //Start Temperatur
  random = +(Math.random() * 60).toFixed(2);

  tempSeries1: TemperatureGaugeDataSeries = {
    name: 'Temperature',
    type: 'gauge',
    data: [this.random]
  }

  TempDataObj: TemperatureGaugeDataSeries = this.tempSeries1;
  //End Temperatur


  //START Switch Button
  statusCards: string;

  lightCard: CardSettings = {
    title: 'Licht',
    iconClass: 'nb-lightbulb',
    type: 'primary',
  };
  rollerShadesCard: CardSettings = {
    title: 'Heizung',
    iconClass: 'nb-flame-circled',
    type: 'warning',
  };

  commonStatusCardsSet: CardSettings[] = [
    this.lightCard,
    this.rollerShadesCard,
  ];

  //Set Theme Design
  statusCardsByThemes: {
    default: CardSettings[];
    cosmic: CardSettings[];
    corporate: CardSettings[];
    dark: CardSettings[];
  } = {
    default: this.commonStatusCardsSet,
    cosmic: this.commonStatusCardsSet,
    corporate: [
      {
        ...this.lightCard,
        type: 'warning',
      },
      {
        ...this.rollerShadesCard,
        type: 'primary',
      }
    ],
    dark: this.commonStatusCardsSet,
  };
  //END Switch Button

  constructor(private theme: NbThemeService,) {
    this.theme.getJsTheme()
    .pipe(takeWhile(() => this.alive))
    .subscribe(theme => {
      this.statusCards = this.statusCardsByThemes[theme.name];
  });
  }

  private alive = true;
  ngOnDestroy() {
    this.alive = false;
  }

  setChartData() {
    console.log("setChartData");
    this.ChartDataObj = this.ChartDataObj2;
    //Zufällige Temperatur
    this.random = +(Math.random() * 60).toFixed(2);
    this.tempSeries1 = {
      name: 'Temperature',
      type: 'gauge',
      data: [this.random]
    }
  
    this.TempDataObj = this.tempSeries1;
  }
}
