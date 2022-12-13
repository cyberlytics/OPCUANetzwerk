import { Injectable, OnInit } from "@angular/core";
import { HttpClient, HttpParams } from '@angular/common/http';
import { AppSettings } from "../statics/AppSettings";


@Injectable()
export class BackendDataService implements OnInit {

    //new http client
    constructor(private http: HttpClient) { }

    ngOnInit(): void {}

    //function to get data from backend the host is defined in the folder static in the file AppSettings.ts
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
            params = params.append('startTimestamp', startTimestamp.toISOString());
        }
        if (endTimestamp) {
            params = params.append('endTimestamp', endTimestamp.toISOString());
        }

        var response = await this.http.get(AppSettings.API_ENDPOINT + '/sensorvalues', { params: params }).toPromise<any>();
        return response;
    }

}

