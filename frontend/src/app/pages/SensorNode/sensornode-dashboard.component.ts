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
import { DashboardFunctionalityService } from '../../Services/DashboardFunctionalityService.service';
import { AirQualityData } from './AirQuality/AirQualityChart/air-quality-data';
import { AirQualityTableData } from './AirQuality/air-quality-list-data';
import { convertUpdateArguments } from '@angular/compiler/src/compiler_util/expression_converter';



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


  //End Gantt


  constructor(private theme: NbThemeService, 
              private backendApi: BackendDataService, 
              private route: ActivatedRoute, 
              private router: Router, 
              private timespan: TimespanService,
              private dashboard: DashboardFunctionalityService) {
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

  ganttData = {
    "xAxis": [],
    "yAxis": ["Presence"],
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

    //Get Sensornode Data
    var resultAir = await this.backendApi.getNodeData(this.SensorNodeId, "BME280", "AirPressure", this.selectedTimespan.from, this.selectedTimespan.to);
    var resultTemp = await this.backendApi.getNodeData(this.SensorNodeId, "BME280", "Temperature", this.selectedTimespan.from, this.selectedTimespan.to);
    var resultHumidity = await this.backendApi.getNodeData(this.SensorNodeId, "BME280", "Humidity", this.selectedTimespan.from, this.selectedTimespan.to);
    let resultPresence = await this.backendApi.getNodeData(this.SensorNodeId, "HRSR501", "Presence", this.selectedTimespan.from, this.selectedTimespan.to);
    var resultAirQuality = await this.backendApi.getNodeData(this.SensorNodeId, "MQ135", "AirQuality", this.selectedTimespan.from, this.selectedTimespan.to);


    //Structure Array: [[timestamp, value]]
    let mappedAir = this.dashboard.mapResult(resultAir);
    let mappedTemp = this.dashboard.mapResult(resultTemp);
    let mappedHumidity = this.dashboard.mapResult(resultHumidity);
    let mappedPresence = this.dashboard.mapResult(resultPresence);
    let mappedAirQuality = this.dashboard.mapResult(resultAirQuality);


    //Start: In Bearbeitung 
    let ganttArr = []
    let tempArr = []
    let present = false;
    let absent = false;

    for (let i = 0; i < mappedPresence.length; i++) {
      for (let j = 0; j < mappedPresence[i].length; j++) {
        if (mappedPresence[i][1] == 0) {
          tempArr.push(mappedPresence[i][0]);
          absent = true;
          if (absent == true && present == true) {
            present = false;
            absent = false;
            ganttArr.push([tempArr[0], tempArr[tempArr.length - 1], 1])
            tempArr = []
            tempArr.push(mappedPresence[i][0]);
          }
        }
        else if (mappedPresence[i][1] == 1) {
          tempArr.push(mappedPresence[i][0]);
          present = true;
          if (absent == true && present == true) {
            present = false;
            absent = false;
            ganttArr.push([tempArr[0], tempArr[tempArr.length - 1], 0])
            tempArr = []
            tempArr.push(mappedPresence[i][0]);
          }
        }
        else {
          console.log("No Value! What happened?");
        }
      }
    }
    //End: In Bearbeitung 



    //Convert Date to ISO String
    mappedAir = this.dashboard.convertMappedDate(mappedAir)
    mappedHumidity = this.dashboard.convertMappedDate(mappedHumidity)
    mappedHumidity = this.dashboard.convertMappedDate(mappedHumidity)
    ganttArr = this.dashboard.convertMappedDate(ganttArr)
    mappedAirQuality = this.dashboard.convertMappedDate(mappedAirQuality)


    //New instances of LineChartDataSeries 
    let newAir: LineChartDataSeries = this.dashboard.lineChartData("AirPressure", mappedAir);
    let newTemp: LineChartDataSeries = this.dashboard.lineChartData("Temperature", mappedTemp);
    let newHumidity: LineChartDataSeries = this.dashboard.lineChartData("Humidity", mappedHumidity);

    this.AirPresure = newAir;
    this.Temperature = newTemp;
    this.Humidity = newHumidity;


    let newPresence = this.dashboard.gantData(ganttArr);
    this.ganttData = newPresence;


    //AirQuality Part:
    //log all the timestamps in an array
    var timestamps = resultAirQuality.map(function (el) {
      return el.timestamp;
    });

    //New instance of AirQualityData
    var newAirQuality: AirQualityData = {
      data: mappedAirQuality
    };

    this.AirQuality = newAirQuality;

    var newAirQualityTable = this.dashboard.calculateAirQualityTableData(this.AirQuality);
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

  async ngAfterViewInit() {
  }

  test() {
  }

  fromChange() { }

  test2() { }


}
