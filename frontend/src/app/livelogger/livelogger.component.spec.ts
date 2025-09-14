import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LiveloggerComponent } from './livelogger.component';

describe('LiveloggerComponent', () => {
  let component: LiveloggerComponent;
  let fixture: ComponentFixture<LiveloggerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LiveloggerComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(LiveloggerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
