import { Injectable } from "@angular/core";
import { BehaviorSubject } from "rxjs";

@Injectable()
export class SharedDataService {
    constructor() { }

    private source = new BehaviorSubject<{from: Date, to: Date}>(null);

    currentTimespan = this.source.asObservable();

    async updateTimespanData(from: Date, to: Date) {
        var output = {
            from: from,
            to: to
        };
        this.source.next(output);
    }

}