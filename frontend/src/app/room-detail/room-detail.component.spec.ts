import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RoomDetailComponent } from './room-detail.component';
import { RouterTestingModule } from '@angular/router/testing';
import { MeetServiceSpy } from '../services/meet.service.spy';
import { MeetService } from '../services/meet.service';
import { RouterLinkStubDirective } from '../../testing/router-stubs';
import { FormsModule } from '@angular/forms';
import { ClipboardModule } from 'ngx-clipboard/dist';

describe('RoomDetailComponent', () => {
  let component: RoomDetailComponent;
  let fixture: ComponentFixture<RoomDetailComponent>;
  let meetServiceSpy: MeetServiceSpy;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports : [
        RouterTestingModule,
        FormsModule,
        ClipboardModule
      ],
      declarations : [
        RoomDetailComponent,
      ],
      providers : [
        { provide : MeetService, useClass : MeetServiceSpy }
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RoomDetailComponent);
    component = fixture.componentInstance;
    meetServiceSpy = fixture.debugElement.injector.get(MeetService) as any;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
