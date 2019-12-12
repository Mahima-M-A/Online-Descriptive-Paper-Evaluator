import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { QPComponent } from './qp.component';

describe('QPComponent', () => {
  let component: QPComponent;
  let fixture: ComponentFixture<QPComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ QPComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(QPComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
