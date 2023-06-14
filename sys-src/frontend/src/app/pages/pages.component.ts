import { Component, OnInit } from '@angular/core';
import { BackendDataService } from '../Services/BackendDataService';

import { MENU_ITEMS } from './pages-menu';

@Component({
  selector: 'ngx-pages',
  styleUrls: ['pages.component.scss'],
  template: `
    <ngx-one-column-layout>
      <nb-menu [items]="menu"></nb-menu>
      <router-outlet></router-outlet>
    </ngx-one-column-layout>
  `,
})
export class PagesComponent implements OnInit {


  constructor(private backendAPI: BackendDataService) {}

  async ngOnInit(): Promise<void> {
    var Nodes: string[] = await this.backendAPI.getSensorNodes();

    //push a new menu item for each node
    Nodes.forEach(element => {
      MENU_ITEMS.push({
        title: element,
        link: element,
        icon: 'home-outline',
      });
    });

  }
  


  menu = MENU_ITEMS;
}
