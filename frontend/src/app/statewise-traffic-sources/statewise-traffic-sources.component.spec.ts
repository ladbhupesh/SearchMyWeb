import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StatewiseTrafficSourcesComponent } from './statewise-traffic-sources.component';

describe('StatewiseTrafficSourcesComponent', () => {
  let component: StatewiseTrafficSourcesComponent;
  let fixture: ComponentFixture<StatewiseTrafficSourcesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ StatewiseTrafficSourcesComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(StatewiseTrafficSourcesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
