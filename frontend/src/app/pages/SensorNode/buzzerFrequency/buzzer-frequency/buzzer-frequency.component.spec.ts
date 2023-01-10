import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BuzzerFrequencyComponent } from './buzzer-frequency.component';

describe('BuzzerFrequencyComponent', () => {
  let component: BuzzerFrequencyComponent;
  let fixture: ComponentFixture<BuzzerFrequencyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BuzzerFrequencyComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BuzzerFrequencyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
