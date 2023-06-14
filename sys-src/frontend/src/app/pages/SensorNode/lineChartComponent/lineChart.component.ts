import {ChangeDetectionStrategy, Component, Input, OnChanges, OnDestroy, SimpleChanges} from '@angular/core';
import { NbThemeService } from '@nebular/theme';
import { takeWhile } from 'rxjs/operators' ;
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
    this.data = changes.data.currentValue;
    this.refreshOptions();
  }

  @Input() data: LineChartDataSeries[];

  options: EChartsOption = {};
  themeSubscription: any;

  ngAfterViewInit() {
    this.themeSubscription = this.theme.getJsTheme().subscribe(config => {


      const colors: any = config.variables;
      const echarts: any = config.variables.echarts;

      this.options = {
        backgroundColor: echarts.bg,
        responsive: true,
        color: [colors.danger, colors.primary, colors.info],
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          textStyle: {
            color: echarts.textColor,
          }
        },
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
            type: 'value',
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
      console.log("textcolor", echarts.textColor)

      
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
