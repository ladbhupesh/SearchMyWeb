import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UpdateCellComponent } from './update-cell.component';

describe('UpdateCellComponent', () => {
  let component: UpdateCellComponent;
  let fixture: ComponentFixture<UpdateCellComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UpdateCellComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UpdateCellComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
