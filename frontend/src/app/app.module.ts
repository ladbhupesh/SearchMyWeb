import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { SignupComponent } from './signup/signup.component';
import { HomeComponent } from './home/home.component';
import { ManageIndexesComponent } from './manage-indexes/manage-indexes.component';
import { TestSearchComponent } from './test-search/test-search.component';
import { SelectSearchComponent } from './select-search/select-search.component';
import { TrafficSourcesComponent } from './traffic-sources/traffic-sources.component';
import { StatewiseTrafficSourcesComponent } from './statewise-traffic-sources/statewise-traffic-sources.component';
import { AnalyticsComponent } from './analytics/analytics.component';
import { WordcloudComponent } from './wordcloud/wordcloud.component';
import { LiveloggerComponent } from './livelogger/livelogger.component';
import { CheckAuthService } from './check-auth.service';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { HttpClientModule } from '@angular/common/http';
import { ListAllUrlsComponent } from './list-all-urls/list-all-urls.component';
import { AgGridModule } from 'ag-grid-angular';
import { BooleanCellComponent } from './boolean-cell/boolean-cell.component';
import { UpdateCellComponent } from './update-cell/update-cell.component';
import { DeleteCellComponent } from './delete-cell/delete-cell.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ToastrModule } from 'ngx-toastr';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    SignupComponent,
    HomeComponent,
    ManageIndexesComponent,
    TestSearchComponent,
    SelectSearchComponent,
    TrafficSourcesComponent,
    StatewiseTrafficSourcesComponent,
    AnalyticsComponent,
    WordcloudComponent,
    LiveloggerComponent,
    ListAllUrlsComponent,
    BooleanCellComponent,
    UpdateCellComponent,
    DeleteCellComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    NgbModule,
    HttpClientModule,
    FontAwesomeModule,
    AgGridModule.withComponents([]),
    ToastrModule.forRoot(),
  ],
  providers: [CheckAuthService],
  bootstrap: [AppComponent],
  entryComponents:[BooleanCellComponent, UpdateCellComponent, DeleteCellComponent],
  
})
export class AppModule { }
