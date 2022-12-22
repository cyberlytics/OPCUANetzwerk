import { Component, OnDestroy, OnInit } from '@angular/core';
import { NbMediaBreakpointsService, NbMenuService, NbSidebarService, NbThemeService } from '@nebular/theme';

import { UserData } from '../../../@core/data/users';
import { LayoutService } from '../../../@core/utils';
import { map, takeUntil } from 'rxjs/operators';
import { interval, Subject, Subscription } from 'rxjs';
import { type } from 'os';
import { TimespanService } from '../../../Services/TimespanProviderService';


@Component({
  selector: 'ngx-header',
  styleUrls: ['./header.component.scss'],
  templateUrl: './header.component.html',
})
export class HeaderComponent implements OnInit, OnDestroy {

  private destroy$: Subject<void> = new Subject<void>();
  userPictureOnly: boolean = false;
  user: any;
  fromPicker: any;
  checked: boolean = false;

  subscription: Subscription;
  intervalId: number;

  toggle(event: any) {
    console.log(event);
  }

  themes = [
    {
      value: 'default',
      name: 'Light',
    },
    {
      value: 'dark',
      name: 'Dark',
    },
    {
      value: 'cosmic',
      name: 'Cosmic',
    },
    {
      value: 'corporate',
      name: 'Corporate',
    },
  ];

  currentTheme = 'default';

  userMenu = [{ title: 'Profile' }, { title: 'Log out' }];

  constructor(private sidebarService: NbSidebarService,
    private menuService: NbMenuService,
    private themeService: NbThemeService,
    private userService: UserData,
    private layoutService: LayoutService,
    private breakpointService: NbMediaBreakpointsService,
    private timespanservice: TimespanService) {
  }

  ngOnInit() {
    this.currentTheme = this.themeService.currentTheme;

    this.userService.getUsers()
      .pipe(takeUntil(this.destroy$))
      .subscribe((users: any) => this.user = users.nick);

    const { xl } = this.breakpointService.getBreakpointsMap();
    this.themeService.onMediaQueryChange()
      .pipe(
        map(([, currentBreakpoint]) => currentBreakpoint.width < xl),
        takeUntil(this.destroy$),
      )
      .subscribe((isLessThanXl: boolean) => this.userPictureOnly = isLessThanXl);

    this.themeService.onThemeChange()
      .pipe(
        map(({ name }) => name),
        takeUntil(this.destroy$),
      )
      .subscribe(themeName => this.currentTheme = themeName);

    this.setDefaultTimespan();

    const source = interval(5000);
    this.subscription = source.subscribe(val => this.updateLiveDates());
  }

  updateLiveDates(){
    if(!this.checked){
      return;
    }

    //set the to date to the current date
    this.ToDate = new Date();
    this.timespanservice.updateData(this.FromDate, this.ToDate);
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }

  changeTheme(themeName: string) {
    this.themeService.changeTheme(themeName);
  }

  toggleSidebar(): boolean {
    this.sidebarService.toggle(true, 'menu-sidebar');
    this.layoutService.changeLayoutSize();

    return false;
  }

  navigateHome() {
    this.menuService.navigateHome();
    return false;
  }

  FromDate: Date;
  ToDate: Date;

  ok() {
    //convert time string to date
    var FromDate_date = this.FromDate;
    var ToDate_date = this.ToDate;

    this.timespanservice.updateData(FromDate_date, ToDate_date);
  }

  //Sets the from date to the beginning of the current week, sets the to date to the current date
  setDefaultTimespan() {
    this.ToDate = new Date();

    var today = new Date();
    var day = today.getDay();
    var diff = today.getDate() - day + (day == 0 ? -6 : 1); // adjust when day is sunday
    var monday = new Date(today.setDate(diff));
    monday.setHours(0, 0, 0, 0);
    this.FromDate = monday;

    this.timespanservice.updateData(this.FromDate, this.ToDate);
  }
}
