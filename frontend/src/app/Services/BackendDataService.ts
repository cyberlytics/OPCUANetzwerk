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
            params = params.append('startTimestamp', this.toLocalISOString(startTimestamp));
        }
        if (endTimestamp) {
            params = params.append('endTimestamp', this.toLocalISOString(endTimestamp));
        }

        var response = await this.http.get(AppSettings.API_ENDPOINT + '/sensorvalues', { params: params }).toPromise<any>();
        return response;
    }

    //TODO: BACKEND MUSS ALLE SESNORKNOTEN AUSGEBEN
    //Diese Methode ist viel zu aufwendig
    async getSensorNodes() {
        var response = await this.http.get(AppSettings.API_ENDPOINT + '/sensorvalues').toPromise<any>();

        var data = response;

        //find all unique sensornodes from data and return them
        var sensornodes = data.map(x => x.sensornode).filter((value, index, self) => self.indexOf(value) === index);
        return sensornodes;
    }

    //function to convert a date to the local time in iso format
    toLocalISOString(date: Date) {
        var tzoffset = (new Date()).getTimezoneOffset() * 60000; //offset in milliseconds
        var localISOTime = (new Date(date.getTime() - tzoffset)).toISOString().slice(0, -1);
        return localISOTime;
    }
}
