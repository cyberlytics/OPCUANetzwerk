import {Component, Input, OnChanges, OnDestroy, SimpleChanges} from '@angular/core';
import { NbThemeService } from '@nebular/theme';
import { colorSets } from '@swimlane/ngx-charts';
import {echarts} from 'echarts';
import { EChartsOption } from 'echarts';
import { TemperatureGaugeDataSeries } from './temperatureGaugeData';

@Component({
  selector: 'TemperatureGauge',
  templateUrl: './temperatureGauge.component.html'
})
export class TemperatureGaugeComponent implements OnDestroy, OnChanges {

  echartsIntance: any;
  keys: any;
  value: any;
  
  constructor(private theme: NbThemeService,) {}

  ngOnChanges(changes: SimpleChanges): void {
    this.options.series = changes.data.currentValue;
    this.refreshOptions();
  }

  @Input() data: TemperatureGaugeDataSeries[];
  @Input() unit: string;

  options: EChartsOption = {};
  themeSubscription: any;

  ngAfterViewInit() {

    this.themeSubscription = this.theme.getJsTheme().subscribe(config => {

      console.log("config changed", config);

      const colors: any = config.variables;
      const echarts: any = config.variables.echarts;
   
      //get value
      this.keys = Object.keys(this.data)
      this.value = this.keys.map(k => this.data[k])


      this.options = {
        series: [
          {
            type: this.value[1],
            center: ['50%', '65%'],
            startAngle: 200,
            endAngle: -20,
            radius: '100%',
            min: 0,
            max: 60,
            splitNumber: 12,
            grid:{
              left: '10%',
              right: '10%',
              top: 50,
              bottom: 50
            },
            progress: {
              show: true,
              width: 20,
            },
            itemStyle: {
              color: colors.primary
            },
            detail: {
              valueAnimation: true,
              fontSize: 30,
              fontWeight: 'bolder',
              formatter: '{value} '+this.unit,
              color: colors.primary
            },
            pointer: {
              length: '60%'
            },
            axisLine: {
              lineStyle: {
                width: 10,
                color: [
                  [0.5, colors.info],
                  [0.7, colors.warning],
                  [1, colors.danger]
                ]
              }
            },
            splitLine: {
              distance: -30,
              length: 10,
              lineStyle: {
                color: echarts.bg,
                width: 4
              }
            },
            axisTick: {
              distance: -30,
              length: 8,
              lineStyle: {
                color: echarts.bg,
                width: 2
              }
            },

            data: [
              {
                value: this.value[2],
                color: colors.primary,
              }
            ]
          }
        ]
      };


      this.refreshOptions();
      console.log("options", this.options);
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



