import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { NbGlobalPhysicalPosition, NbToastrService } from '@nebular/theme';
import { BackendDataService } from '../../../Services/BackendDataService';

enum InputError {
  NoError = 0,
  InputTooLong = 1,
  InputContainsNonAsciiCharacters = 2
}

@Component({
  selector: 'lcd-input',
  templateUrl: './lcd-input.component.html',
  styleUrls: ['./lcd-input.component.scss']
})
export class LcdInputComponent implements OnInit, OnChanges{

  constructor(private backendAPI: BackendDataService,private toastrService: NbToastrService) { }

  @Input() SensorNode: string;

  status1: string = "primary";
  status2: string = "primary";
  buttonStatus: string = "primary";

  state1: InputError = InputError.NoError;
  state2: InputError = InputError.NoError;

  input_data1: string = "";
  input_data2: string = "";

  ngOnInit(): void {
    this.getSensorNodeValues()
  }

  ngOnChanges(changes: SimpleChanges): void {
    this.getSensorNodeValues()
  }

  getSensorNodeValue(node, actor, value) {
    return this.backendAPI.getActorValue(node, actor, value);
  }

  getSensorNodeValues(){
    //get the sensor node value of the text line for the LCD 1602A
    var res1 = this.getSensorNodeValue(this.SensorNode, "1602A", "TextLine1")
    var res2 = this.getSensorNodeValue(this.SensorNode, "1602A", "TextLine2")

    //wait for both requests to finish
    Promise.all([res1, res2]).then((values) => {
    //values[0] is the result of the first request and values[1] the second request
      this.input_data1 = values[0];
      this.input_data2 = values[1];

      //if the first request returns a value, set the input data and status
      if(values[0] != null){
        this.change1(values[0]);
      }else{
        this.input_data1 = "";
        this.status1 = "primary";
      }

      //if the second request returns a value, set the input data and status
      if(values[1] != null){
        this.change2(values[1]);
      }else{
        this.input_data2 = "";
        this.status2 = "primary";
      }

    }).catch((error) => {
      this.showToast("danger", "LCD-Text update failed", error);
    });
  }
  
  async onSubmit(value: any) {

  //check if a SensorNode is selected
  if(!this.SensorNode){
    throw new Error("No SensorNode selected");
  }

  //check if both inputs are valid
  if(!this.bothInputsValid()){

    //for every state of the two inputs display an appropriate toast
    if(this.state1 == InputError.InputContainsNonAsciiCharacters){
      this.showToast("danger", "Upper Input not correct", "Input contains non-ascii characters");
    }else if(this.state1 == InputError.InputTooLong){
      this.showToast("danger", "Upper Input not correct", "Input is too long");
    }else if(this.state2 == InputError.InputContainsNonAsciiCharacters){
      this.showToast("danger", "Lower Input not correct", "Input contains non-ascii characters");
    }else if(this.state2 == InputError.InputTooLong){
      this.showToast("danger", "Lower Input not correct", "Input is too long");
    }

  }else{
    //send the two inputs to the backend
    var response1 = await this.backendAPI.sendPutRequest(this.SensorNode, "1602A","TextLine1", this.input_data1);
    var response2 = await this.backendAPI.sendPutRequest(this.SensorNode, "1602A","TextLine2", this.input_data2);

    //check if the backend responded with success
    if(response1 == null && response2 == null){
      this.showToast("success", "LCD-Text updated", "Success");
    }else{
      //display the error message from the backend
      this.showToast("danger", "LCD-Text update failed", response1.status + " " + response1.statusText+ " | " + response2.status + " " + response2.statusText);
    }
  }
}

  showToast(type: string, message: string, title: string){
  // 1. Create a configuration object for the toastr
  const config = {
    status: type,
    destroyByClick: true,
    duration: 10000,//10s in ms 
    hasIcon: true,
    position: NbGlobalPhysicalPosition.TOP_RIGHT,
    preventDuplicates: false,
  };
  // 2. Call the toastrService with the message, title, and configuration
  this.toastrService.show(message, title, config);
  }





  //Input may only contain ascii characters
  //Input may only be 16 characters long
  checkInput(input: string): InputError {
    var cut = this.cutInput(input);
    
    // check if input is longer than 16 characters
    if (cut.length > 16) {
        return InputError.InputTooLong;
    }
    
    // check if input contains non-ascii characters
    for (var i = 0; i < input.length; i++) {
        if (cut.charCodeAt(i) > 127) {
            return InputError.InputContainsNonAsciiCharacters;
        }
    }
    
    // return no error if all checks pass
    return InputError.NoError;
  }

  //function to cut the part between < and > from the string
  // cutInput is a function that takes a string as an input
  cutInput(input: string){
    // Find the index of the start of the first tag
    var start = input.indexOf("<");
    // Find the index of the end of the first tag
    var end = input.indexOf(">");
    // Check if the string has any tags
    if(start == -1 || end == -1){
      // If not, return the string
      return input;
    }
    // Return the string without the tag
    var cut = input.substring(0, start) + input.substring(end + 1);
    return cut
  }

  handleInputError(error: InputError, status: string) {
  }

  bothInputsValid(): boolean {
    return this.state1 == InputError.NoError && this.state2 == InputError.NoError;
  }


  //Add this function to the component class
  change1(event: any){
    //Check the input and store the result
    this.state1 = this.checkInput(event);

    //Set the status to danger if the input is invalid
    switch (this.state1) {
      case InputError.InputTooLong:
        this.status1 = "danger";
        break;
      case InputError.InputContainsNonAsciiCharacters:
        this.status1 = "danger";
        break;
      case InputError.NoError:
        this.status1 = "success";
        break;
    }

    if(this.bothInputsValid()){
      this.buttonStatus = "success";
    }else{
      this.buttonStatus = "danger";
    }
  }
  change2(event: any){
    this.state2 = this.checkInput(event);
    switch (this.state2) {
      case InputError.InputTooLong:
        this.status2 = "danger";
        break;
      case InputError.InputContainsNonAsciiCharacters:
        this.status2 = "danger";
        break;
      case InputError.NoError:
        this.status2 = "success";
        break;
    }

    if(this.bothInputsValid()){
      this.buttonStatus = "success";
    }else{
      this.buttonStatus = "danger";
    }
  }

}
