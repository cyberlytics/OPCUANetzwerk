import { delay, takeWhile } from 'rxjs/operators';
import { AfterViewInit, Component, Input, OnDestroy, SimpleChanges } from '@angular/core';
import { NbThemeService } from '@nebular/theme';
import { LayoutService } from '../../../../@core/utils';
import { ElectricityChart } from '../../../../@core/data/electricity';
import { LineChartDataSeries } from '../../lineChartComponent/LineChartDataClass';
import { AirQualityData } from './air-quality-data';
import { EChartsOption } from 'echarts';


@Component({
  selector: 'air-quality-chart',
  styleUrls: ['./air-quality-chart.component.scss'],
  template: `
    <div echarts
         [options]="option"
         [merge]="option"
         class="echart"
         (chartInit)="onChartInit($event)">
    </div>
  `,
})
export class AirQualityChartComponent implements AfterViewInit, OnDestroy {

  private alive = true;

  //@Input() data: ElectricityChart[];
  @Input() data: AirQualityData;


  option: EChartsOption = {};
  echartsIntance: any;

  constructor(private theme: NbThemeService,
              private layoutService: LayoutService) {
    this.layoutService.onSafeChangeLayoutSize()
      .pipe(
        takeWhile(() => this.alive),
      )
      .subscribe(() => this.resizeChart());
  }

  ngOnChanges(changes: SimpleChanges): void {
    this.data = changes.data.currentValue;

    //set the data in the options for every series in the options
    if(this.option.series == undefined)
      return;
    else{
      for (let i = 0; i < this.option.series.length; i++) {
        this.option.series[i].data = this.data.data;
      }
    }
    
    this.refreshOptions();
  }


  ngAfterViewInit(): void {
    this.theme.getJsTheme()
      .pipe(
        takeWhile(() => this.alive),
        delay(1),
      )
      .subscribe(config => {
        const eTheme: any = config.variables.electricity;

        this.option = {
          grid: {
            left: 0,
            top: 0,
            right: 0,
            bottom: 80,
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'line',
              lineStyle: {
                color: eTheme.tooltipLineColor,
                width: eTheme.tooltipLineWidth,
              },
            },
            textStyle: {
              color: eTheme.tooltipTextColor,
              fontSize: 20,
              fontWeight: eTheme.tooltipFontWeight,
            },
            position: 'top',
            backgroundColor: eTheme.tooltipBg,
            borderColor: eTheme.tooltipBorderColor,
            borderWidth: 1,
            //formatter to show the date and the value in [] in the tooltip
            formatter: (params) => {
              const date = new Date(params[0].data[0]);
              const dateString = date.toLocaleDateString('en-US', {year: 'numeric', month: 'long', day: 'numeric'});
              const timeString = date.toLocaleTimeString('en-US', {hour: 'numeric', minute: 'numeric', hour12: true});
              return dateString + ' ' + timeString + ' ' + params[0].data[1] +"ppm";
            },
            extraCssText: eTheme.tooltipExtraCss,
          },
          xAxis: {
            type: 'time',
            boundaryGap: true,
            offset: 25,
            axisTick: {
              show: false,
            },
            axisLabel: {
              color: eTheme.xAxisTextColor,
              fontSize: 18,
            },
            axisLine: {
              lineStyle: {
                color: eTheme.axisLineColor,
                width: '2',
              },
            },
          },
          yAxis: {
            boundaryGap: [0, '5%'],
            axisLine: {
              show: false,
            },
            axisLabel: {
              show: false,
            },
            axisTick: {
              show: false,
            },
            splitLine: {
              show: true,
              lineStyle: {
                color: eTheme.yAxisSplitLine,
                width: '1',
              },
            },
          },
          series: [
            {
              type: 'line',
              smooth: true,
              symbolSize: 20,
              itemStyle: {
                normal: {
                  opacity: 0,
                },
                emphasis: {
                  color: '#ffffff',
                  borderColor: eTheme.itemBorderColor,
                  borderWidth: 2,
                  opacity: 1,
                },
              },
              lineStyle: {
                normal: {
                  width: eTheme.lineWidth,
                  type: eTheme.lineStyle,
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: eTheme.lineGradFrom,
                  }, {
                    offset: 1,
                    color: eTheme.lineGradTo,
                  }]),
                  shadowColor: eTheme.lineShadow,
                  shadowBlur: 6,
                  shadowOffsetY: 12,
                },
              },
              areaStyle: {
                normal: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: eTheme.areaGradFrom,
                  }, {
                    offset: 1,
                    color: eTheme.areaGradTo,
                  }]),
                },
              },
              data: this.data.data
            },

            {
              type: 'line',
              smooth: true,
              symbol: 'none',
              lineStyle: {
                normal: {
                  width: eTheme.lineWidth,
                  type: eTheme.lineStyle,
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: eTheme.lineGradFrom,
                  }, {
                    offset: 1,
                    color: eTheme.lineGradTo,
                  }]),
                  shadowColor: eTheme.shadowLineDarkBg,
                  shadowBlur: 14,
                  opacity: 1,
                },
              },
              data: this.data.data,
            },
          ],
        };
    });
  }

  refreshOptions() {
    if(this.echartsIntance) {
      this.echartsIntance.setOption(this.option);
    }
  }
  
  onChartInit(echarts) {
    this.echartsIntance = echarts;
  }

  resizeChart() {
    if (this.echartsIntance) {
      this.echartsIntance.resize();
    }
  }

  ngOnDestroy() {
    this.alive = false;
  }
}
