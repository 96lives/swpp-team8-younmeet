import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { SuiModule } from 'ng2-semantic-ui';
import { DashboardComponent } from './dashboard/dashboard.component';
import { RoomListComponent } from './dashboard/room-list/room-list.component';

@NgModule({
  declarations : [
    AppComponent,
    DashboardComponent,
    RoomListComponent
  ],
  imports : [
    BrowserModule,
    SuiModule
  ],
  providers : [],
  bootstrap : [ AppComponent ]
})
export class AppModule {}