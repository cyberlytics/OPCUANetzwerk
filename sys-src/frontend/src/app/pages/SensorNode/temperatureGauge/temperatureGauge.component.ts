import {Component, Input, OnChanges, OnDestroy, SimpleChanges} from '@angular/core';
import { NbThemeService } from '@nebular/theme';
import { colorSets } from '@swimlane/ngx-charts';
import {echarts} from 'echarts';
import { EChartsOption } from 'echarts';

@Component({
  selector: 'TemperatureGauge',
  templateUrl: './temperatureGauge.component.html'
})
export class TemperatureGaugeComponent implements OnDestroy, OnChanges {

  echartsIntance: any;
  
  constructor(private theme: NbThemeService,) {}

  ngOnChanges(changes: SimpleChanges): void {

    //if data or unit changed for the first time, do nothing
    if(changes.data != undefined){
      if(changes.data.firstChange == true) return;
    }
    if(changes.unit != undefined){
      if(changes.unit.firstChange == true) return;
    };

    //if data or unit changed, update the gauge
    //round trhe value to 2 decimal places
    var rounded = changes.data.currentValue.toFixed(2);
    this.data = rounded;
    this.options.series[0].data[0].value = rounded;
    this.refreshOptions();
  }

  // @Input() data: TemperatureGaugeDataSeries;
  @Input() data: number;
  @Input() unit: string;
  @Input() title?: string;
  //inputs for min and max values
  @Input() min: number = 0;
  @Input() max: number = 60;

  options: EChartsOption = {};
  themeSubscription: any;

  ngAfterViewInit() {


    this.themeSubscription = this.theme.getJsTheme().subscribe(config => {


      const colors: any = config.variables;
      const echarts: any = config.variables.echarts;

      this.options = {
        series: [
          {
            type: 'gauge',
            center: ['50%', '65%'],
            startAngle: 200,
            endAngle: -20,
            radius: '100%',
            min: this.min,
            max: this.max,
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
                value: this.data,
                color: colors.primary,
              }
            ]
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



