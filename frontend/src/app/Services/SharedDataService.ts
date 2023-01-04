import { Injectable } from "@angular/core";
import { BehaviorSubject } from "rxjs";

@Injectable()
export class SharedDataService {
    constructor() { }

    private source = new BehaviorSubject<{from: Date, to: Date}>(null);
    private sourceId = new BehaviorSubject<string>(null);


    currentTimespan = this.source.asObservable();
    currentSensorNode = this.sourceId.asObservable();


    async updateTimespanData(from: Date, to: Date) {
        var output = {
            from: from,
            to: to
        };
        this.source.next(output);
    }

    async updateSensorNode(nodeId: string) {
        var output = nodeId;
        this.sourceId.next(output);
    }

}