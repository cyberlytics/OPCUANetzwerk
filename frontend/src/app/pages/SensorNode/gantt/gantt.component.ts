import { ChangeDetectionStrategy, Component, ElementRef, Input, OnChanges, OnDestroy, SimpleChanges, ViewChild } from '@angular/core';
import { NbThemeService } from '@nebular/theme';
import { takeWhile } from 'rxjs/operators';
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
export class GanttComponent implements OnDestroy, OnChanges{

  constructor(private theme: NbThemeService,) { }

  ngOnChanges(changes: SimpleChanges): void {
    if(changes.data.firstChange){
      return
    }
    this.options.yAxis.data = changes.data.currentValue.yAxis
    this.options.series[0].data = changes.data.currentValue.xAxis
    this.data = changes.data.currentValue;    
    this.refreshOptions();
    console.log(this.data)
  }

  @Input() data: any;

  options: EChartsOption = {};
  themeSubscription: any;
  echartsIntance: any;


  ngAfterViewInit() {

    this.themeSubscription = this.theme.getJsTheme().subscribe(config => {
      const colors: any = config.variables;
      const echarts: any = config.variables.echarts;

      const valveColors = [
        "#f59527",
        "#00e200",
        "#2da8f3",
      ]

      function renderItem(params, api) {        
        var catIndex = api.value(2);
        var timeSpan = [api.value(0), api.value(1)];        
        var start = api.coord([timeSpan[0], 2 - catIndex]);        
        var end = api.coord([timeSpan[1], 2 - catIndex]);
        var size = api.size([0, 1]);
        var height = size[1] * 0.6;
        var rect = echartsObj.graphic.clipRectByRect(
          { x: start[0], y: start[1] - height / 2, width: end[0] - start[0], height: height },
          { x: params.coordSys.x, y: params.coordSys.y, width: params.coordSys.width, height: params.coordSys.height }
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
      }

      //Diagramm Optionen definieren
      this.options = {
        title: {
          left: 'center'
        },
        xAxis: {
          type: 'time',
          min: range => range.min - (1 * 24 * 60 * 60 * 1000), //Subtract 7 days
          max: range => range.max + (1 * 24 * 60 * 60 * 1000), //Subtract 7 days
             boundaryGap:false,
            axisLine: {
              lineStyle: {
                color: echarts.axisLineColor,
              },
            }
        },
        yAxis: {
          type: "category",
          data: this.data.yAxis,
          axisLine: {
            lineStyle: {
              color: echarts.axisLineColor,
            },
          },
          splitLine: {
            lineStyle: {
              color: echarts.splitLineColor,
            },
          },
          axisLabel: {
            textStyle: {
              color: echarts.textColor,
            },
          },
        },
        series: [
          {
            type: "custom",
            renderItem: renderItem,
            encode: {
              x: [0, 1],
              y: 0,
            },
            data: this.data.xAxis,
          }
        ],
        tooltip: {
          show: true,
          trigger: "item",
          formatter: params => {
            //hover Box
            return `${params.data.name}<br/> ${params.data.value[0]} - ${params.data.value[1]}` //Unix timestamps should be converted to readable dates
          }
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
    if (this.echartsIntance) {
      this.echartsIntance.setOption(this.options);
    }
  }

  private alive = true;
  ngOnDestroy() {
    this.alive = false;
  }

}
