import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'lcd-input',
  templateUrl: './lcd-input.component.html',
  styleUrls: ['./lcd-input.component.scss']
})
export class LcdInputComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

  onSubmit(value: any) {
    //get the value from the input field with id="input"
    var input = document.getElementById("input") as HTMLInputElement;

    //if the input is empty do nothing
    if (input.value == "") {
      return;
    }

    //TODO: send the value to the backend
    throw new Error("Not implemented");
  }

}
