import {ChangeDetectionStrategy, Component, ElementRef, Input, OnChanges, OnDestroy, SimpleChanges, ViewChild} from '@angular/core';
import { NbThemeService } from '@nebular/theme';
import { takeWhile } from 'rxjs/operators' ;
import { SolarData } from '../../../@core/data/solar';
//import {echarts} from 'echarts';
import * as echartsObj from 'echarts';
import { EChartsOption } from 'echarts';
import * as moment from 'moment';

@Component({
  selector: 'Gantt',
  templateUrl: './gantt.component.html',
  styleUrls: ['./gantt.component.scss']
})
export class GanttComponent {
  


  echartsIntance: any;
  @ViewChild('gantt') span:ElementRef;

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
      const colors: any = config.variables;
      const echarts: any = config.variables.echarts;

      //Gantt Beispiele
      //https://stackoverflow.com/questions/73300725/apache-echarts-schedule-style-chart-layout
      //https://echarts.apache.org/examples/en/editor.html?c=custom-profile&reset=1&edit=1


      

      var data = [];
      var dataCount = 10;
      var startTime = +new Date();
      var categories = ['categoryA', 'categoryB', 'categoryC'];
      var types = [
        { name: 'JS Heap', color: '#7b9ce1' },
        { name: 'Documents', color: '#bd6d6c' },
        { name: 'Nodes', color: '#75d874' },
        { name: 'Listeners', color: '#e0bc78' },
        { name: 'GPU Memory', color: '#dc77dc' },
        { name: 'GPU', color: '#72b362' }
      ];
      // Generate mock data
      categories.forEach(function (category, index) {
        var baseTime = startTime;
        for (var i = 0; i < dataCount; i++) {
          var typeItem = types[Math.round(Math.random() * (types.length - 1))];
          var duration = Math.round(Math.random() * 10000);
          data.push({
            name: typeItem.name,
            value: [index, baseTime, (baseTime += duration), duration],
            itemStyle: {
              normal: {
                color: typeItem.color
              }
            }
          });
          baseTime += Math.round(Math.random() * 2000);
        }
      });
      function renderItem(params, api) {
        var categoryIndex = api.value(0);
        var start = api.coord([api.value(1), categoryIndex]);
        var end = api.coord([api.value(2), categoryIndex]);
        var height = api.size([0, 1])[1] * 0.6;

        var rectShape;

        
        var rectShape = echartsObj.graphic.clipRectByRect(
          {
            x: start[0],
            y: start[1] - height / 2,
            width: end[0] - start[0],
            height: height
          },
          {
            x: params.coordSys.x,
            y: params.coordSys.y,
            width: params.coordSys.width,
            height: params.coordSys.height
          }
        );
        
        return (
          rectShape && {
            type: 'rect',
            transition: ['shape'],
            shape: rectShape,
            style: api.style()
          }
        );
      }


      this.options = {
        tooltip: {
          formatter: function (params) {
            return params.marker + params.name + ': ' + params.value[3] + ' ms';
          }
        },
        title: {
          text: 'Profile',
          left: 'center'
        },
        dataZoom: [
          {
            type: 'slider',
            filterMode: 'weakFilter',
            showDataShadow: false,
            top: 400,
            labelFormatter: ''
          },
          {
            type: 'inside',
            filterMode: 'weakFilter'
          }
        ],
        grid: {
          height: 300
        },
        xAxis: {
          min: startTime,
          scale: true,
          axisLabel: {
            formatter: function (val) {
              return Math.max(0, val - startTime) + ' ms';
            }
          }
        },
        yAxis: {
          data: categories
        },
        series: [
          {
            type: 'custom',
            renderItem: renderItem,
            itemStyle: {
              opacity: 0.8
            },
            encode: {
              x: [1, 2],
              y: 0
            },
            data: data
          }
        ]
  
      };

      this.refreshOptions();
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
      this.echartsIntance.setOption(this.options);
    }
  }
  
  private alive = true;
  ngOnDestroy() {
    this.alive = false;
  }

}
