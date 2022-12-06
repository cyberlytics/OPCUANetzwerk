import {ChangeDetectionStrategy, Component, Input, OnChanges, OnDestroy, SimpleChanges} from '@angular/core';
import { NbThemeService } from '@nebular/theme';
import { takeWhile } from 'rxjs/operators' ;
import { SolarData } from '../../../@core/data/solar';
import {echarts} from 'echarts';
import { EChartsOption } from 'echarts';
import * as moment from 'moment';
import { LineChartDataSeries } from './LineChartDataClass';

@Component({
  selector: 'LineChart',
  styleUrls: ['./lineChart.component.scss'],
  templateUrl: './lineChart.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LineChartComponent implements OnDestroy, OnChanges {


  echartsIntance: any;

  constructor(private theme: NbThemeService,) {}

  ngOnChanges(changes: SimpleChanges): void {
    this.options.series = changes.data.currentValue;
    this.refreshOptions();
  }

  @Input() data: LineChartDataSeries[];

  options: EChartsOption = {};
  themeSubscription: any;

  ngAfterViewInit() {

    this.themeSubscription = this.theme.getJsTheme().subscribe(config => {

      console.log("config changed");

      const colors: any = config.variables;
      const echarts: any = config.variables.echarts;

      this.options = {
        backgroundColor: echarts.bg,
        responsive: true,
        color: [colors.danger, colors.primary, colors.info],
        tooltip: {
          trigger: 'axis'
        },
        legend: {        },
        xAxis: [
          {
             type: 'time',
             boundaryGap:false,
            axisLine: {
              lineStyle: {
                color: echarts.axisLineColor,
              },
            },
            axisLabel: {
              textStyle: {
                color: echarts.textColor,
              },
              formatter: (function(value){
                  return moment(value).format('DD.MM.yyyy HH:mm:ss');
              })
            },
          },
        ],
        yAxis: [
          {
            type: 'log',
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
        ],
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true,
        },
        series: this.data
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
