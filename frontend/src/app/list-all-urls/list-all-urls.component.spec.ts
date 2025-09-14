import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListAllUrlsComponent } from './list-all-urls.component';

describe('ListAllUrlsComponent', () => {
  let component: ListAllUrlsComponent;
  let fixture: ComponentFixture<ListAllUrlsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ListAllUrlsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ListAllUrlsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
