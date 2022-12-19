import { Injectable } from "@angular/core";
import { BehaviorSubject } from "rxjs";

@Injectable()
export class TimespanService {
    constructor() { }

    private source = new BehaviorSubject<{from: Date, to: Date}>(null);

    currentData = this.source.asObservable();

    async updateData(from: Date, to: Date) {
        var output = {
            from: from,
            to: to
        };
        this.source.next(output);
    }

}