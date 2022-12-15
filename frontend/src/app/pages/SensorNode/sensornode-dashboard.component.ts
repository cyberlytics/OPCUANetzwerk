import {Component, OnDestroy, OnInit} from '@angular/core';
import { NbThemeService } from '@nebular/theme';
import { takeWhile } from 'rxjs/operators' ;
import { SolarData } from '../../@core/data/solar';
import { BackendDataService } from '../../Services/BackendDataService';
import {  LineChartDataSeries } from './lineChartComponent/LineChartDataClass';
import { Subscription } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import {Router} from '@angular/router';
import { TimespanService } from '../../Services/TimespanProviderService';



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
  };

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

  tempSeries1: number = this.random;

  TempDataObj = this.tempSeries1;
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

//  Temperature: LineChartDataSeries = {
//     name: "Temperature",
//     type: "line",
//     //10 Random Values for data
//     data: [["2018-08-15T10:04:01.339Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-16T10:14:13.914Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-17T10:04:01.339Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-18T10:14:13.914Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-19T10:04:01.339Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-20T10:14:13.914Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-21T10:04:01.339Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-22T10:14:13.914Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-23T10:04:01.339Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-24T10:14:13.914Z",Math.round(Math.random()* 100* 100) / 100]]
//   }
//   Humidity: LineChartDataSeries = {
//     name: "Humidity",
//     type: "line",
//     //10 Random Values for data
//     data: [["2018-08-15T10:04:01.339Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-16T10:14:13.914Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-17T10:04:01.339Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-18T10:14:13.914Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-19T10:04:01.339Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-20T10:14:13.914Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-21T10:04:01.339Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-22T10:14:13.914Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-23T10:04:01.339Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-24T10:14:13.914Z",Math.round(Math.random()* 100* 100) / 100]]
//   }
//   AirPresure: LineChartDataSeries = {
//     name: "Air Presure",
//     type: "line",
//     //10 Random Values for data
//     data: [["2018-08-15T10:04:01.339Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-16T10:14:13.914Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-17T10:04:01.339Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-18T10:14:13.914Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-19T10:04:01.339Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-20T10:14:13.914Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-21T10:04:01.339Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-22T10:14:13.914Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-23T10:04:01.339Z",Math.round(Math.random()* 100* 100) / 100],["2018-08-24T10:14:13.914Z",Math.round(Math.random()* 100* 100) / 100]]
//   }

  Temperature: LineChartDataSeries = {
    name: "Temperature",
    type: "line",
    //10 Random Values for data
    data: []
  }
  Humidity: LineChartDataSeries = {
    name: "Humidity",
    type: "line",
    //10 Random Values for data
    data: []
  }
  AirPresure: LineChartDataSeries = {
    name: "Air Presure",
    type: "line",
    //10 Random Values for data
    data: []
  }
  
  
  gaugeRandom : number = 10;

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

  async getData(){
    
    var resultAir = await this.backendApi.getNodeData(this.SensorNodeId, "BME280", "AirPressure",this.selectedTimespan.from,this.selectedTimespan.to);
    var resultTemp = await this.backendApi.getNodeData(this.SensorNodeId, "BME280", "Temperature",this.selectedTimespan.from,this.selectedTimespan.to );
    var resultHumidity = await this.backendApi.getNodeData(this.SensorNodeId, "BME280", "Humidity",this.selectedTimespan.from,this.selectedTimespan.to );

    //create an array from the result where the elements are structured like this [[timestamp, value]]
    var mappedAir = resultAir.map(function(el) {
      return [el.timestamp, el.value];
    });

    var mappedTemp = resultTemp.map(function(el) {
      return [el.timestamp, el.value];
    });

    var mappedHumidity = resultHumidity.map(function(el) {
      return [el.timestamp, el.value];
    });

    //We need new instances of LineChartDataSeries because only changing the properties of it does not trigger the change detection
    //this is because the reference to the object does not change

    var newAir = new LineChartDataSeries();
    newAir.name = "AirPressure";
    newAir.type = "line";
    newAir.data = mappedAir;

    var newTemp = new LineChartDataSeries();
    newTemp.name = "Temperature";
    newTemp.type = "line";
    newTemp.data = mappedTemp;

    var newHumidity = new LineChartDataSeries();
    newHumidity.name = "Humidity";
    newHumidity.type = "line";
    newHumidity.data = mappedHumidity;

    this.AirPresure = newAir;
    this.Temperature = newTemp;
    this.Humidity = newHumidity;

  }

  private subscription: Subscription;
  private SensorNodeId: string;

  async ngOnInit(): Promise<void> {
    console.log("SensorNodeDashboardComponent ngOnInit");
    this.subscription = this.route.paramMap.subscribe(async params => { 
      var id = params.get('id');
      this.SensorNodeId = id;    
      console.log("NODE ID", id);
      

      //Check if the Nodeid mathces one in the database, redirect to 404 if not
      var validNodes = await this.backendApi.getSensorNodes();

      //if the nodeId does not match one of the valid nodes, redirect to 404
      var found = validNodes.some(function (el) {
        return el == id;
      }); 
      if(!found){
        this.router.navigate(['/pages/not-found']);
      }


      this.getData();
  });

  this.timespan.currentData.subscribe(data => {
    this.selectedTimespan = data;
    console.log("timespan changed", data);
    this.getData();
  });
  }

  async ngAfterViewInit() {
  }

  test(){
    console.log(this.selectedTimespan)
  }

  fromChange(){
    console.log("AAAs")
  }

  test2(){
    console.log("test2")
  }
}
