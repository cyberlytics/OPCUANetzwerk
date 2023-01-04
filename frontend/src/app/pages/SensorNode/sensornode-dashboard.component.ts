import { Component, OnDestroy, OnInit } from '@angular/core';
import { NbThemeService } from '@nebular/theme';
import { takeWhile } from 'rxjs/operators';
import { BackendDataService } from '../../Services/BackendDataService';
import { LineChartDataSeries } from './lineChartComponent/LineChartDataClass';
import { Subscription } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import { Router } from '@angular/router';
import { SharedDataService } from '../../Services/SharedDataService';
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


  constructor(private theme: NbThemeService, 
              private backendApi: BackendDataService, 
              private route: ActivatedRoute, 
              private router: Router, 
              private sharedData: SharedDataService,
              private dashboard: DashboardFunctionalityService) {
    this.theme.getJsTheme()
      .pipe(takeWhile(() => this.alive))
      .subscribe(theme => {
        this.statusCards = this.statusCardsByThemes[theme.name];
      });
  }


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
    if (this.selectedTimespan.from == null || this.selectedTimespan.to == null || this.dashboard.isCorrectDate(this.selectedTimespan.from) == false || this.dashboard.isCorrectDate(this.selectedTimespan.to) == false) {
      return;
    }

    //Get Sensornode Data
    var resultAir = await this.backendApi.getNodeData(this.SensorNodeId, "BME280", "AirPressure", this.selectedTimespan.from, this.selectedTimespan.to);
    var resultTemp = await this.backendApi.getNodeData(this.SensorNodeId, "BME280", "Temperature", this.selectedTimespan.from, this.selectedTimespan.to);
    var resultHumidity = await this.backendApi.getNodeData(this.SensorNodeId, "BME280", "Humidity", this.selectedTimespan.from, this.selectedTimespan.to);
    let resultPresence = await this.backendApi.getNodeData(this.SensorNodeId, "HRSR501", "Presence", this.selectedTimespan.from, this.selectedTimespan.to);
    var resultAirQuality = await this.backendApi.getNodeData(this.SensorNodeId, "MQ135", "AirQuality", this.selectedTimespan.from, this.selectedTimespan.to);

    //convert the values from Air hpa into bar
    for (let i = 0; i < resultAir.length; i++) {
      resultAir[i].value = resultAir[i].value / 1000;
    }




    
    //Structure Array: [[timestamp, value]]
    let mappedAir = this.dashboard.mapResult(resultAir);
    let mappedTemp = this.dashboard.mapResult(resultTemp);
    let mappedHumidity = this.dashboard.mapResult(resultHumidity);
    let mappedPresence = this.dashboard.mapResult(resultPresence);
    let mappedAirQuality = this.dashboard.mapResult(resultAirQuality);




    mappedPresence = this.dashboard.cleanMotianData(mappedPresence);



    // console.log("CLEANED", mappedPresence);


    //var finalGantt = this.dashboard.generateMotionDataset(mappedPresence);

    // console.log("GANTT", finalGantt);


    let ganttArr = this.dashboard.gantArray(mappedPresence)
    


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
    //APPLY NEW FIX newPresence.xAxis = finalGantt;
    this.ganttData = newPresence;   

    //console.log("ganttdata", newPresence);
    


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
      this.sharedData.updateSensorNode(id); 

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

    this.sharedData.currentTimespan.subscribe(data => {
      this.selectedTimespan = data;
      this.getData();
    });
  }


  async ngAfterViewInit() {
  }

  test() {
  }

  fromChange() { }

  test2() { }


}
