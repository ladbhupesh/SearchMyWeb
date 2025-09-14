import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageIndexesComponent } from './manage-indexes.component';

describe('ManageIndexesComponent', () => {
  let component: ManageIndexesComponent;
  let fixture: ComponentFixture<ManageIndexesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ManageIndexesComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ManageIndexesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
