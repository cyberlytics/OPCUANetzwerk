import { Component, Input } from '@angular/core';

@Component({
  selector: 'Switch',
  templateUrl: './switch.component.html',
  styleUrls: ['./switch.component.scss']
})
export class SwitchComponent {

  @Input() title: string;
  @Input() type: string;
  @Input() on = true;

}
