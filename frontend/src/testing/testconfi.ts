import { HttpClient, HttpHandler, HttpClientModule } from "@angular/common/http";
import { FormsModule } from "@angular/forms";
import { BrowserModule } from "@angular/platform-browser";
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { NbThemeService, NbToastrService, NbCardModule, NbUserModule, NbButtonModule, NbTabsetModule, NbActionsModule, NbRadioModule, NbSelectModule, NbListModule, NbIconModule, NbInputModule, NbToastrModule, NbOverlayModule, NbSidebarModule, NbMenuModule, NbDatepickerModule, NbTimepickerModule, NbDialogModule, NbWindowModule, NbChatModule } from "@nebular/theme";
import { NgxEchartsModule } from "ngx-echarts";
import { CoreModule } from "../app/@core/core.module";
import { ThemeModule } from "../app/@theme/theme.module";
import { AppRoutingModule } from "../app/app-routing.module";
import { BackendDataService } from "../app/Services/BackendDataService";

export const testConfig = {
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

}