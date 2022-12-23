import { Injectable, OnInit } from "@angular/core";
import { HttpClient, HttpParams } from '@angular/common/http';
import { AppSettings } from "../statics/AppSettings";


@Injectable()
export class BackendDataService implements OnInit {

    //new http client
    constructor(private http: HttpClient) { }

    ngOnInit(): void {}

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

        var response = await this.http.get(AppSettings.API_ENDPOINT_PI + '/sensorvalues', { params: params }).toPromise<any>();
        return response;
    }

    async getSensorNodes() {
        var response = await this.http.get(AppSettings.API_ENDPOINT_PI + '/sensornodes').toPromise<any>();
        return response;
    }

    async getActorValue(sensornode: string, actuatorname: string, actuator_act: string) {
        var response = await this.http.get(AppSettings.API_ENDPOINT_PI + '/actuators/').toPromise<any>();

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

        var response = await this.http.put(AppSettings.API_ENDPOINT_PI + '/actuators/', payload).toPromise<any>();
        return response;
    }
}
