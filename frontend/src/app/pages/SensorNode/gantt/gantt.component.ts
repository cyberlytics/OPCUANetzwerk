import {ChangeDetectionStrategy, Component, Input, OnChanges, OnDestroy, SimpleChanges} from '@angular/core';
import { NbThemeService } from '@nebular/theme';
import { takeWhile } from 'rxjs/operators' ;
import { SolarData } from '../../../@core/data/solar';
import {echarts} from 'echarts';
import { EChartsOption } from 'echarts';
import * as moment from 'moment';

@Component({
  selector: 'Gantt',
  templateUrl: './gantt.component.html',
  styleUrls: ['./gantt.component.scss']
})
export class GanttComponent {


  echartsIntance: any;

  constructor(private theme: NbThemeService,) {}

  ngOnChanges(changes: SimpleChanges): void {
    this.options.series = changes.data.currentValue;
    this.refreshOptions();
  }

 // @Input() data: LineChartDataSeries[];

  options: EChartsOption = {};
  themeSubscription: any;

  ngAfterViewInit() {

    this.themeSubscription = this.theme.getJsTheme().subscribe(config => {

      console.log("config changed");

      const colors: any = config.variables;
      const echarts: any = config.variables.echarts;

      //Gantt Beispiele
      //https://stackoverflow.com/questions/73300725/apache-echarts-schedule-style-chart-layout
      //https://echarts.apache.org/examples/en/editor.html?c=custom-profile&reset=1&edit=1

      const valveColors = [
        "#f59527",
        "#00e200",
        "#2da8f3",
    ]
    
    var data = [
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
    ];

      this.options = {
        xAxis: {
          type: "time",
  //Min is getting values from index 1, not sure why
          min: range => range.min - (7 * 24 * 60 * 60 * 1000), //Subtract 7 days
      },
      yAxis: {
          type: "category",
          data: [ "Valve 3", "Valve 2", "Valve 1" ]
      },
      series: [
          {
              type: "custom",
              renderItem: (params, api) => {
                  var catIndex = api.value(2);
                  var timeSpan = [api.value(0), api.value(1)];
                  var start = api.coord([timeSpan[0], 2 - catIndex]);
                  var end = api.coord([timeSpan[1], 2 -catIndex]);
                  var size = api.size([0,1]);
                  var height = size[1] * 0.6;
                  //echarts = undefined Fehler taucht auf (zeichnet die balken die gefüllt werden)
                  /*var rect = echarts.graphic.clipRectByRect(
                      { x: start[0], y: start[1] - height / 2, width: end[0] - start[0], height: height},
                      { x: params.coordSys.x, y: params.coordSys.y, width: params.coordSys.width, height: params.coordSys.height}
                  );
                  return (
                      rect && {
                          type: "rect",
                          transition: ["shape"],
                          shape: rect,
                          style: {
                              fill: valveColors[catIndex],
                          },
                      }
                  );
                  */
              },
              encode: {
                  x: [0,1],
                  y: 0,
              },
              data: data,
          }
      ],
      tooltip: {
          show: true,
          trigger: "item",
          formatter: params => {
              return `${params.data.name}<br/> ${params.data.value[0]} - ${params.data.value[1]}` //Unix timestamps should be converted to readable dates
          }
      },
      dataZoom: [
          {
              type: "slider",
              filterMode: "none"
          },
      ],
  
      };

      this.refreshOptions();
      console.log("options2", this.options);
      
    });

  }

  onChartInit(echarts) {
    this.echartsIntance = echarts;
  }

  
  resizeChart() {
    if (this.echartsIntance) {
      this.echartsIntance.resize();
    }
  }

  refreshOptions() {
    if(this.echartsIntance) {
      console.log("options2", this.options);

      this.echartsIntance.setOption(this.options);
    }
  }
  
  private alive = true;
  ngOnDestroy() {
    this.alive = false;
  }

}
