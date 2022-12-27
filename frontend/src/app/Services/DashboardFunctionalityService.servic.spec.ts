import { HttpClient, HttpHandler, HttpClientModule } from '@angular/common/http';
import { SimpleChange } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NbThemeService, NbToastrService, NbCardModule, NbUserModule, NbButtonModule, NbTabsetModule, NbActionsModule, NbRadioModule, NbSelectModule, NbListModule, NbIconModule, NbInputModule, NbToastrModule, NbOverlayModule, NbSidebarModule, NbMenuModule, NbDatepickerModule, NbTimepickerModule, NbDialogModule, NbWindowModule, NbChatModule } from '@nebular/theme';
import { NgxEchartsModule } from 'ngx-echarts';
import { CoreModule } from '../@core/core.module';
import { ThemeModule } from '../@theme/theme.module';
import { AppRoutingModule } from '../app-routing.module';
import { LineChartDataSeries } from '../pages/SensorNode/lineChartComponent/LineChartDataClass';
import { BackendDataService } from '../Services/BackendDataService';
import { DashboardFunctionalityService } from './DashboardFunctionalityService.service';

//create a test file for the component
describe('DashboardFuncionalityService', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      providers: [BackendDataService, HttpClient, NbThemeService, HttpHandler, NbToastrService,],
      imports: [
        FormsModule,
        ThemeModule,
        NbCardModule,
        NbUserModule,
        NbButtonModule,
        NbTabsetModule,
        NbActionsModule,
        NbRadioModule,
        NbSelectModule,
        NbListModule,
        NbIconModule,
        NbButtonModule,
        NgxEchartsModule,
        NbInputModule,
        NbToastrModule.forRoot(),
        NbOverlayModule.forRoot(),
        BrowserModule,
        BrowserAnimationsModule,
        HttpClientModule,
        AppRoutingModule,
        NbSidebarModule.forRoot(),
        NbMenuModule.forRoot(),
        NbDatepickerModule.forRoot(),
        NbTimepickerModule.forRoot(),
        NbDialogModule.forRoot(),
        NbWindowModule.forRoot(),
        NbChatModule.forRoot({
          messageGoogleMapKey: 'AIzaSyA_wNuCzia92MAmdLRzmqitRGvCF7wCZPY',
        }),
        CoreModule.forRoot(),
        ThemeModule.forRoot(),
      ],

    })
      .compileComponents();
  });

  let dashboard = new DashboardFunctionalityService();

  //mapResult
  it('should map the Data like this: [[timestamp, value]]', () => {
    let unmappedData = [
      {
        sensorname: "BME280",
        sensornode: "SensorNode_2",
        sensortyp: "AirPressure",
        timestamp: "2022-12-26T00:01:16.609000",
        unit: "hPa",
        value: 0.9718927784688763
      },
      {
        sensorname: "BME280",
        sensornode: "SensorNode_2",
        sensortyp: "AirPressure",
        timestamp: "2022-12-26T00:04:16.657000",
        unit: "hPa",
        value: 0.9719581225185164
      }
    ]

    let expected = [
      [
        "2022-12-26T00:01:16.609000",
        0.9718927784688763
      ],
      [
        "2022-12-26T00:04:16.657000",
        0.9719581225185164
      ]
    ]

    let mapped = dashboard.mapResult(unmappedData);
    expect(mapped).toEqual(expected);
  });


  //cleanMotianData
  it('cleans excess 1s and 0s Ganttdata [[timestamp, value]]', () => {
    let uncleaned = [
      ["2022-12-26T00:42:42.852000", 1],
      ["2022-12-26T01:42:46.088000", 1],
      ["2022-12-26T01:43:48.262000", 0]
    ]

    let expected = [
      ["2022-12-26T00:42:42.852000", 1],
      ["2022-12-26T01:43:48.262000", 0]
    ]

    let cleaned = dashboard.cleanMotianData(uncleaned);
    expect(cleaned).toEqual(expected);
  });

  //gantArray
  it('should save the start and end timestamp with the value', () => {
    let data = [
      ["2022-12-26T00:42:42.852000", 1],
      ["2022-12-26T00:43:45.013000", 0],
      ["2022-12-26T01:42:46.088000", 1]
    ]

    let expected = [
      ["2022-12-26T00:42:42.852000", "2022-12-26T00:43:45.013000", 1],
      ["2022-12-26T00:43:45.013000", "2022-12-26T01:42:46.088000", 0]
    ]

    let gantt = dashboard.gantArray(data);
    expect(gantt).toEqual(expected);
  });


  //convertMappedDate
  it('should change the data as a ISO-String', () => {
    let mapped = [
      [
        "2022-12-26T00:01:16.609000",
        0.9718927784688763
      ],
      [
        "2022-12-26T00:04:16.657000",
        0.9719581225185164
      ]
    ]

    let mappedString = dashboard.convertMappedDate(mapped);
    expect(mappedString).toEqual(mapped);
  });


  //convertMappedDate
  it('should convert the timestamp and value to a LineChartDataSeries', () => {
    let mapped = [
      [
        "2022-12-26T00:01:16.609000",
        0.9718927784688763
      ],
      [
        "2022-12-26T00:04:16.657000",
        0.9719581225185164
      ]
    ]

    let lineChartData: LineChartDataSeries = {
      name: "AirPressure",
      type: "line",
      data: [
        [
          "2022-12-26T00:01:16.609000",
          0.9718927784688763
        ],
        [
          "2022-12-26T00:04:16.657000",
          0.9719581225185164
        ]
      ]
    }

    let expected = dashboard.lineChartData("AirPressure", mapped);
    expect(expected).toEqual(lineChartData);
  });



  //calculateAirQualityTableData



  //isDateCorrect
  it('if Date is valid then false will be returned', () => {
    let valid = "2022-12-26T00:01:16.609000"
    let expected = dashboard.isCorrectDate(valid);
    expect(expected).toEqual(false);
  });

  //gantData
  it('should convert the starttimestamp and endtimestamp and value to a GanttData', () => {
    let value = [
      "2022-12-25T23:42:42.852Z", "2022-12-26T00:43:45.013000", 1
    ]

    let expectedGanttData = {
      "xAxis": [
        {
          name: "Presence",
          value: ["2022-12-25T23:42:42.852Z", "2022-12-26T00:43:45.013000", 1]
        }
      ],
      "yAxis": ["Presence"],
    }

    let expected = dashboard.gantData([value]);    
    expect(expected).toEqual(expectedGanttData);
  });

});
