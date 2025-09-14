import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TrafficSourcesComponent } from './traffic-sources.component';

describe('TrafficSourcesComponent', () => {
  let component: TrafficSourcesComponent;
  let fixture: ComponentFixture<TrafficSourcesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TrafficSourcesComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TrafficSourcesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
