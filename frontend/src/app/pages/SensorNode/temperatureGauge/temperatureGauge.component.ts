import {Component, Input, OnChanges, OnDestroy, SimpleChanges} from '@angular/core';
import { NbThemeService } from '@nebular/theme';
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

  options: EChartsOption = {};
  themeSubscription: any;

  ngAfterViewInit() {

    this.themeSubscription = this.theme.getJsTheme().subscribe(config => {

      const colors: any = config.variables;
      const echarts: any = config.variables.echarts;

      //get value
      this.keys = Object.keys(this.data)
      this.value = this.keys.map(k => this.data[k])


      this.options = {
        series: [
          {
            backgroundColor: echarts.bg,
            color: [colors.danger, colors.primary, colors.info],
            type: this.value[1],
            center: ['50%', '60%'],
            startAngle: 200,
            endAngle: -20,
            min: 0,
            max: 60,
            splitNumber: 12,
            colorBy: '#5470c6',
            progress: {
              show: true,
              width: 10
            },
            itemStyle: {
              color: '#FFAB91'
            },
            detail: {
              valueAnimation: true,
              fontSize: 30,
              fontWeight: 'bolder',
              formatter: '{value} °C',
              color: '#FFAB91'
            },
            pointer: {
              length: '60%'
            },
            data: [
              {
                value: this.value[2],
                color: '#FFAB91',
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



