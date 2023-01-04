import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'led-display',
  templateUrl: './led-display.component.html',
  styleUrls: ['./led-display.component.scss']
})
export class LedDisplayComponent implements OnInit {

  constructor() { }

  @Input() SensorNode: string;

  ngOnInit(): void {

  }

}
