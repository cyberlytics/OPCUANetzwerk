import { Component, Input, OnInit } from '@angular/core';
import { NbGlobalPhysicalPosition, NbToastrService } from '@nebular/theme';
import { BackendDataService } from '../../../../Services/BackendDataService';

@Component({
  selector: 'buzzer-frequency',
  templateUrl: './buzzer-frequency.component.html',
  styleUrls: ['./buzzer-frequency.component.scss']
})
export class BuzzerFrequencyComponent implements OnInit {

  constructor(private toastrService: NbToastrService, private backendAPI: BackendDataService) { }

  input;
  disabled = false;

  @Input() SensorNode: string;

  ngOnInit(): void {
    this.backendAPI.getActorValue(this.SensorNode, "Piezo_1", "ToneFrequency").then((value) => {
      this.input = value;
    });
  }

  //a function to check if the input is a number
  isNumber(value: string): boolean {
    return !isNaN(Number(value));
  }

  change(event: any) {
    if (this.isNumber(event)) {
      this.disabled = false
    }
    else {
      this.disabled = true
    }
  }

  async onSubmit() {
    if(!this.SensorNode){
      throw new Error("No SensorNode selected");
    }

    if(!this.isNumber(this.input)){
      this.showToast("danger", "Input not correct", "Input contains invalid characters or is too long");
      return;
    }

    var response = await this.backendAPI.sendPutRequest(this.SensorNode, "Piezo_1", "ToneFrequency", this.input);

    if(response == null){
      this.showToast("success", "Buzzer frequency updated", "Success");
    }else{
      this.showToast("danger", "Buzzer frequency update failed", response.status + " " + response.statusText);
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
}
