import { Component, Input, OnInit } from '@angular/core';
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
export class LcdInputComponent implements OnInit {

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
  }

  async onSubmit(value: any) {

    if(!this.SensorNode){
      throw new Error("No SensorNode selected");
    }

    if(!this.bothInputsValid()){
      this.showToast("danger", "Input not correct", "Input contains invalid characters or is too long");
    }else{
      var response1 = await this.backendAPI.sendPutRequest(this.SensorNode, "1602A","TextLine1", this.input_data1);
      var response2 = await this.backendAPI.sendPutRequest(this.SensorNode, "1602A","TextLine2", this.input_data2);

      if(response1 == null && response2 == null){
        this.showToast("success", "LCD-Text updated", "Success");
      }else{
        this.showToast("danger", "LCD-Text update failed", response1.status + " " + response1.statusText+ " | " + response2.status + " " + response2.statusText);
      }
    }
  }

  showToast(type: string, message: string, title: string){
    const config = {
      status: type,
      destroyByClick: true,
      duration: 10000,//10s in ms 
      hasIcon: true,
      position: NbGlobalPhysicalPosition.TOP_RIGHT,
      preventDuplicates: false,
    };

    this.toastrService.show(message, title, config);
  }





  //Input may only contain ascii characters
  //Input may only be 16 characters long
  checkInput(input: string): InputError {
    if (input.length > 16) {
      return InputError.InputTooLong;
    }
    for (var i = 0; i < input.length; i++) {
      if (input.charCodeAt(i) > 127) {
        return InputError.InputContainsNonAsciiCharacters;
      }
    }
    return InputError.NoError;
  }

  handleInputError(error: InputError, status: string) {
  }

  bothInputsValid(): boolean {
    return this.state1 == InputError.NoError && this.state2 == InputError.NoError;
  }

  change1(event: any){
    this.state1 = this.checkInput(event);
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
