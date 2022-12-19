import { Component } from '@angular/core';

@Component({
  selector: 'ngx-footer',
  styleUrls: ['./footer.component.scss'],
  template: `
    <span class="created-by">
      Created with ♥ by <b>Team Green</b> for Semantic Web Technologies 2022/23
    </span>
  `,
})
export class FooterComponent {
}
