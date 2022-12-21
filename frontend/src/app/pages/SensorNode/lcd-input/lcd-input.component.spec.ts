import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LcdInputComponent } from './lcd-input.component';

describe('LcdInputComponent', () => {
  let component: LcdInputComponent;
  let fixture: ComponentFixture<LcdInputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LcdInputComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(LcdInputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
