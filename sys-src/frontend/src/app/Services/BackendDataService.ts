import { Injectable, OnInit } from "@angular/core";
import { HttpClient, HttpErrorResponse, HttpParams } from '@angular/common/http';
import { AppSettings } from "../statics/AppSettings";
import { NbGlobalPhysicalPosition, NbToastrService } from "@nebular/theme";


@Injectable()
export class BackendDataService implements OnInit {

    //new http client
    constructor(private http: HttpClient,private toastrService: NbToastrService) {
        this.ngOnInit();
     }

    ApiEndpoint = "http://"+ window.location.hostname+":8000";

    //USE THIS IF YOU ARE ON LOCALHOST IN THE VPN:
    //ApiEndpoint = AppSettings.API_ENDPOINT_PI;


    ngOnInit(): void {
        console.log("API ENDPOINT", this.ApiEndpoint);
    }

   /**
   * function to get data from backend the host is defined in the folder static in the file AppSettings.ts
   * 
   * @param {string}  sensornode - Name des Sensorknoten
   * @param {string} sensorname - Sensorname 
   * @param {string} sensortyp - Sensortyp (AirPressure , ...)
   * @param {Date} startTimestamp - Startdatum nachdem die Daten gefiltert werden
   * @param {Date} endTimestamp - Enddatum nachdem die Daten gefiltert werden
   * 
   */
    async getNodeData(sensornode?: string, sensorname?: string, sensortyp?: string, startTimestamp?: Date, endTimestamp?: Date) {
        let params = new HttpParams();
        //only append the params if they are not null
        if (sensornode) {
            params = params.append('sensornode', sensornode);
        }
        if (sensorname) {
            params = params.append('sensorname', sensorname);
        }
        if (sensortyp) {
            params = params.append('sensortyp', sensortyp);
        }
        if (startTimestamp) {
            params = params.append('startTimestamp', this.toLocalISOString(startTimestamp));
        }
        if (endTimestamp) {
            params = params.append('endTimestamp', this.toLocalISOString(endTimestamp));
        }

        try{
            var response = await this.http.get(this.ApiEndpoint + '/sensorvalues', { params: params }).toPromise<any>();
        }
        catch(error){
            if(error instanceof HttpErrorResponse){
                this.showError(error.message, 'HTTP Requst Failed');
                return [];
            }
        }
        return response;
    }

    async getSensorNodes() {
        try{
            var response = await this.http.get(this.ApiEndpoint + '/sensornodes').toPromise<any>();
        }
        catch(error){
            if(error instanceof HttpErrorResponse){
                this.showError(error.message, 'HTTP Requst Failed');
                return [];
            }
        }
        return response;
    }

    async getActorValue(sensornode: string, actuatorname: string, actuator_act: string) {
        try{
            var response = await this.http.get(this.ApiEndpoint + '/actuators/').toPromise<any>();
        }
        catch(error){
            if(error instanceof HttpErrorResponse){
                this.showError(error.message, 'HTTP Requst Failed');
                return [];
            }
        }

        for (const actuator of response) {
            if(actuator.actuator_node == sensornode + "-" + actuatorname && actuator.actuator_act == actuator_act) {
                return actuator.actuator_value;
            }
        }  
        return response;
    }

    /**
   * function to convert a date to the local time in iso format
   * 
   * @param {Date} date - Das zu formatierende Datum
   * 
   */
    toLocalISOString(date: Date) {
        var tzoffset = (new Date()).getTimezoneOffset() * 60000; //offset in milliseconds
        var localISOTime = (new Date(date.getTime() - tzoffset)).toISOString().slice(0, -1);
        return localISOTime;
    }

    //function to send a put request to an actuator
    async sendPutRequest(sensornode: string, actuatorname: string, actuator_act: string, value: string) {

        var payload = {
            "actuator_node": sensornode + "-" + actuatorname,
            "actuator_act": actuator_act,
            "new_value": value
        }

        try{
            var response = await this.http.put(this.ApiEndpoint + '/actuators/', payload).toPromise<any>();
        }
        catch(error){
            if(error instanceof HttpErrorResponse){
                this.showError(error.message, 'HTTP Requst Failed');
                return -1;
            }
        }
        return response;
    }

    showError(message: string, title: string){
        const config = {
          status: "danger",
          destroyByClick: true,
          duration: 10000,//10s in ms 
          hasIcon: true,
          position: NbGlobalPhysicalPosition.TOP_RIGHT,
          preventDuplicates: true,
        };
    
        this.toastrService.show(message, title, config);
      }
}
