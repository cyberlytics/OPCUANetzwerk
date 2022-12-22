import { Component, OnDestroy, OnInit } from '@angular/core';
import { NbThemeService } from '@nebular/theme';
import { takeWhile } from 'rxjs/operators';
import { SolarData } from '../../@core/data/solar';
import { BackendDataService } from '../../Services/BackendDataService';
import { LineChartDataSeries } from './lineChartComponent/LineChartDataClass';
import { Subscription } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import { Router } from '@angular/router';
import { TimespanService } from '../../Services/TimespanProviderService';
import { AirQualityData } from './AirQuality/AirQualityChart/air-quality-data';
import { AirQualityTableData } from './AirQuality/air-quality-list-data';



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
export class SensorNodeDashboardComponent implements OnDestroy, OnInit {

  selectedTimespan: {
    from: Date,
    to: Date
  }

  Series1: LineChartDataSeries = {
    name: "Series1",
    type: "line",
    data: [["2018-08-15T10:04:01.339Z", 5], ["2018-08-15T10:14:13.914Z", 7]]
  }

  Series2: LineChartDataSeries = {
    name: "Series2",
    type: "line",
    data: [["2018-08-15T10:04:01.339Z", 10], ["2018-08-15T10:14:13.914Z", 15]]
  }


  Series3: LineChartDataSeries = {
    name: "Series3",
    type: "line",
    data: [["2018-08-16T10:04:01.339Z", 23], ["2018-08-16T10:14:13.914Z", 2]]
  }

  Series4: LineChartDataSeries = {
    name: "Series4",
    type: "line",
    data: [["2018-08-16T10:04:01.339Z", 20], ["2018-08-16T10:14:13.914Z", 10]]
  }

  ChartDataObj: LineChartDataSeries[] = [this.Series1, this.Series2];
  ChartDataObj2: LineChartDataSeries[] = [this.Series3, this.Series4];


  //Start Temperatur
  random = +(Math.random() * 60).toFixed(2);

  tempSeries1: number = this.random;

  TempDataObj = this.tempSeries1;
  //End Temperatur


  //START Switch Button
  statusCards: string;

  lightCard: CardSettings = {
    title: 'Light',
    iconClass: 'nb-lightbulb',
    type: 'primary',
  };
  rollerShadesCard: CardSettings = {
    title: 'Heating',
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


  //Start Gantt
  //Aufbau von value: = [v1,v2, v3] (v1 und v2 ergeben die Zeit in ms wie lange jmd anwesend ist, v3 zeigt in welche 
  //Reihe es erfasst wird)







  ganttData = {
    "xAxis":
      [
        {
          "name": "Valve 1",
          "value": [
            1655647200000,
            1657980000000,
            0
          ]
        },
        {
          "name": "Valve 3",
          "value": [
            1657980000000,
            1659448800000,
            2
          ]
        },
        {
          "name": "Valve 1",
          "value": [
            1659448800000,
            1660526144467,
            0
          ]
        },
        {
          "name": "Valve 2",
          "value": [
            1655647200000,
            1660526144467,
            1
          ]
        }
      ],
    "yAxis": ["Value 3", "Value 2", "Value 1"],
  }
  //End Gantt


  constructor(private theme: NbThemeService, private backendApi: BackendDataService, private route: ActivatedRoute, private router: Router, private timespan: TimespanService) {
    this.theme.getJsTheme()
      .pipe(takeWhile(() => this.alive))
      .subscribe(theme => {
        this.statusCards = this.statusCardsByThemes[theme.name];
      });


  }



  //START FLIP CARD
  AirQuality: AirQualityData = {
    data: [],
  }

  AirQualityList: AirQualityTableData[] = [];

  Temperature: LineChartDataSeries = {
    name: "Temperature",
    type: "line",
    data: []
  }
  Humidity: LineChartDataSeries = {
    name: "Humidity",
    type: "line",
    data: []
  }
  AirPresure: LineChartDataSeries = {
    name: "Air Presure",
    type: "line",
    data: []
  }


  gaugeRandom: number = 10;

  //END FLIP CARD
  private alive = true;
  ngOnDestroy() {
    this.alive = false;
  }

  setChartData() {
    // this.ChartDataObj = this.ChartDataObj2;
    // //Zufällige Temperatur
    // this.random = +(Math.random() * 60).toFixed(2);

    // this.tempSeries1 = this.random;
    // this.gaugeRandom = this.random;
    // this.TempDataObj = this.tempSeries1;

    this.getData();
  }

  async getData() {

    //check if both from and to date have values
    if (this.selectedTimespan == null) {
      return;
    }
    if (this.selectedTimespan.from == null || this.selectedTimespan.to == null || this.isCorrectDate(this.selectedTimespan.from) == false || this.isCorrectDate(this.selectedTimespan.to) == false) {
      return;
    }

    var resultAir = await this.backendApi.getNodeData(this.SensorNodeId, "BME280", "AirPressure", this.selectedTimespan.from, this.selectedTimespan.to);
    var resultTemp = await this.backendApi.getNodeData(this.SensorNodeId, "BME280", "Temperature", this.selectedTimespan.from, this.selectedTimespan.to);
    var resultHumidity = await this.backendApi.getNodeData(this.SensorNodeId, "BME280", "Humidity", this.selectedTimespan.from, this.selectedTimespan.to);

    //create an array from the result where the elements are structured like this [[timestamp, value]]
    var mappedAir = resultAir.map(function (el) {
      return [el.timestamp, el.value];
    });

    var mappedTemp = resultTemp.map(function (el) {
      return [el.timestamp, el.value];
    });

    var mappedHumidity = resultHumidity.map(function (el) {
      return [el.timestamp, el.value];
    });

    //get the timestamp of each datapoint and convert it into a date object, the convert the date into an iso string
    //this is needed because the chart component does not support the date format from the backend
    mappedAir.forEach(function (el) {
      var date = new Date(el[0]);
      el[0] = date.toISOString();
    });

    mappedTemp.forEach(function (el) {
      var date = new Date(el[0]);
      el[0] = date.toISOString();
    });

    mappedHumidity.forEach(function (el) {
      var date = new Date(el[0]);
      el[0] = date.toISOString();
    });

    //We need new instances of LineChartDataSeries because only changing the properties of it does not trigger the change detection
    //this is because the reference to the object does not change

    var newAir: LineChartDataSeries = {
      name: "AirPressure",
      type: "line",
      data: mappedAir
    };

    var newTemp: LineChartDataSeries = {
      name: "Temperature",
      type: "line",
      data: mappedTemp
    };

    var newHumidity: LineChartDataSeries = {
      name: "Humidity",
      type: "line",
      data: mappedHumidity
    };

    this.AirPresure = newAir;
    this.Temperature = newTemp;
    this.Humidity = newHumidity;

    //AirQuality Part:
    var resultAirQuality = await this.backendApi.getNodeData(this.SensorNodeId, "MQ135", "AirQuality", this.selectedTimespan.from, this.selectedTimespan.to);

    //log all the timestamps in an array
    var timestamps = resultAirQuality.map(function (el) {
      return el.timestamp;
    });

    //create an array from the result where the elements are structured like this [[timestamp, value]]
    var mappedAirQuality = resultAirQuality.map(function (el) {
      return [el.timestamp, el.value];
    });

    //get the timestamp of each datapoint and convert it into a date object, the convert the date into an iso string
    //this is needed because the chart component does not support the date format from the backend
    mappedAirQuality.forEach(function (el) {
      var date = new Date(el[0]);
      el[0] = date.toISOString();
    });

    var newAirQuality: AirQualityData = {
      data: mappedAirQuality
    };

    this.AirQuality = newAirQuality;

    var newAirQualityTable = this.calculateAirQualityTableData(this.AirQuality);
    this.AirQualityList = newAirQualityTable;
  }

  private subscription: Subscription;
  SensorNodeId: string;

  async ngOnInit(): Promise<void> {
    this.subscription = this.route.paramMap.subscribe(async params => {
      var id = params.get('id');
      this.SensorNodeId = id;

      //Check if the Nodeid mathces one in the database, redirect to 404 if not
      var validNodes = await this.backendApi.getSensorNodes();

      //if the nodeId does not match one of the valid nodes, redirect to 404
      var found = validNodes.some(function (el) {
        return el == id;
      });
      if (!found) {
        this.router.navigate(['/pages/not-found']);
      }


      this.getData();
    });

    this.timespan.currentData.subscribe(data => {
      this.selectedTimespan = data;
      this.getData();
    });
  }

  isCorrectDate(date) {
    if (date instanceof Date) {
      var text = Date.prototype.toString.call(date);
      return text !== 'Invalid Date';
    }
    return false;
  }

  //A function that calculates averages for the air quality for each day. 
  //It also calculates the delata to the day before.
  //It takes data in the form of the Interface AirQualityData and outputs an array in the form of the Interface AirQualityTableData
  //The final data represents average airquality levels for each day and the delta to the day before
  calculateAirQualityTableData(data: AirQualityData): AirQualityTableData[] {

    if(!data || !data.data || data.data.length == 0){
      return [];
    }

    //sort the data by date the date is in string so we need to convert it to a date object before
    data.data.sort(function (a, b) {
      var dateA = new Date(a[0]);
      var dateB = new Date(b[0]);
      return dateA.getTime() - dateB.getTime();
    });

    //now we need to group the data by day
    var dayGroup = [];
    data.data.forEach(function (el) {
      var date = new Date(el[0]);
      var day = date.getDate();
      var month = date.getMonth()+1;
      var year = date.getFullYear();

      var dayString = day + "." + month + "." + year;

      if (!dayGroup[dayString]) {
        dayGroup[dayString] = [];
      }
      dayGroup[dayString].push(el[1]);
    });

    //now we need to calculate the average for each day
    var result2 = [];
    for (var key in dayGroup) {
      var sum = 0;
      var count = 0;
      dayGroup[key].forEach(function (el) {
        sum += el;
        count++;
      });

      result2.push({
        day: key,
        average: sum / count
      });
    }

    //on the first element on the array we set the delta to 0
    result2[0].delta = 0;

    //now we need to calculate the delta to the day before
    for (var i = 1; i < result2.length; i++) {
      var delta = result2[i].average - result2[i - 1].average;
      result2[i].delta = delta;
      //if the delta is positive, we add set the down attribute to false, if it is negative we set it to true
      result2[i].down = delta < 0;
    }

    return result2;
  }
    
  


  async ngAfterViewInit() {
  }

  test() {
  }

  fromChange() { }

  test2() { }


}
