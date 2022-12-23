import { HttpClient, HttpHandler, HttpClientModule } from '@angular/common/http';
import { SimpleChange } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NbThemeService, NbToastrService, NbCardModule, NbUserModule, NbButtonModule, NbTabsetModule, NbActionsModule, NbRadioModule, NbSelectModule, NbListModule, NbIconModule, NbInputModule, NbToastrModule, NbOverlayModule, NbSidebarModule, NbMenuModule, NbDatepickerModule, NbTimepickerModule, NbDialogModule, NbWindowModule, NbChatModule } from '@nebular/theme';
import { NgxEchartsModule } from 'ngx-echarts';
import { CoreModule } from '../../../@core/core.module';
import { ThemeModule } from '../../../@theme/theme.module';
import { AppRoutingModule } from '../../../app-routing.module';
import { BackendDataService } from '../../../Services/BackendDataService';
import { LineChartComponent } from './lineChart.component';
import { LineChartDataSeries } from './LineChartDataClass';

//create a test file for the component
describe('LineChartComponent', () => {
    let component: LineChartComponent;
    let fixture: ComponentFixture<LineChartComponent>;
    
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
    
    beforeEach(() => {
        fixture = TestBed.createComponent(LineChartComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });
    
    it('should create', () => {
        expect(component).toBeTruthy();
    });

    //Test if the chart refreshes when the input changes
    it('should refresh chart when input changes', () => {
        const spy = spyOn(component, 'refreshOptions');
        var data : LineChartDataSeries = {
            name: "test",
            type: "line",
            data: [["2022-12-22T15:27:32.171000",3]]
        }

        component.ngOnChanges({
            data: new SimpleChange(null, [data], false),
        });

        expect(spy).toHaveBeenCalled();

        expect(component.options.series).toEqual([data]);
    });

});
