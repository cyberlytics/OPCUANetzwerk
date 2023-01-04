import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { interval, Subscription } from 'rxjs';
import { BackendDataService } from '../../../Services/BackendDataService';

//enum for green, red, yellow and blue
enum LedColor {
  Green = 1,
  Red,
  Yellow,
  Blue
}


@Component({
  selector: 'led-display',
  templateUrl: './led-display.component.html',
  styleUrls: ['./led-display.component.scss']
})
export class LedDisplayComponent implements OnInit, OnChanges{

  constructor(private backendAPI: BackendDataService) { }

  @Input() SensorNode: string;


  //get the elements of the leds

  greenLed: HTMLElement;
  redLed: HTMLElement;
  yellowLed: HTMLElement;
  blueLed: HTMLElement;
  subscription: Subscription;

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.SensorNode) {
      this.getLedValues();    
    }
  }



  ngOnInit(): void {
  }

  ngAfterViewInit(): void {
    //get the Led elements
    this.greenLed = document.getElementById("greenLed");
    this.redLed = document.getElementById("redLed");
    this.yellowLed = document.getElementById("yellowLed");
    this.blueLed = document.getElementById("blueLed");

    //get the state of the leds every 10 seconds
    const source = interval(10000);
    this.subscription = source.subscribe(val => this.getLedValues());
  }

  getLedValues() {
    if (!this.SensorNode) {
      throw new Error("No SensorNode selected");
    }

    var greenValue = this.backendAPI.getActorValue(this.SensorNode, "LED_Stripe_1", "GreenLED");
    var redValue = this.backendAPI.getActorValue(this.SensorNode, "LED_Stripe_1", "RedLED");
    var yellowValue = this.backendAPI.getActorValue(this.SensorNode, "LED_Stripe_1", "OrangeLED");
    var blueValue = this.backendAPI.getActorValue(this.SensorNode, "LED_Stripe_1", "BlueLED");

    Promise.all([greenValue, redValue, yellowValue, blueValue]).then((values) => {

      this.changeLedState(this.greenLed, values[0], LedColor.Green);
      this.changeLedState(this.redLed, values[1], LedColor.Red);
      this.changeLedState(this.yellowLed, values[2], LedColor.Yellow);
      this.changeLedState(this.blueLed, values[3], LedColor.Blue);
    });

  }

  //this 
  changeLedState(led: HTMLElement, state: boolean, color: LedColor) {
    if (!this.SensorNode) {
      throw new Error("No SensorNode selected");
    }

    var styleColorOn: string;
    var styleColorOff: string;


    switch (color) {
      case LedColor.Green:
        styleColorOn = "#00ff00";
        styleColorOff = "#006000"
        break;
      case LedColor.Red:
        styleColorOn = "#ff0000";
        styleColorOff = "#600000"
        break;
      case LedColor.Yellow:
        styleColorOn = "#ffff00";
        styleColorOff = "#606000"
        break;
      case LedColor.Blue:
        styleColorOn = "#0000ff";
        styleColorOff = "#000060"
        break;
    }


    if (state) {
      led.style.backgroundColor = styleColorOn;
      led.style.boxShadow = "0 0 10px " + styleColorOn;
    }
    else {
      led.style.backgroundColor = styleColorOff;
      led.style.boxShadow = "none";
    }

  }

}
