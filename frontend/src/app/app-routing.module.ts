import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AlreadyAuthServiceService } from './already-auth-service.service';
import { AnalyticsComponent } from './analytics/analytics.component';
import { CheckAuthService } from './check-auth.service';
import { HomeComponent } from './home/home.component';
import { LiveloggerComponent } from './livelogger/livelogger.component';
import { LoginComponent } from './login/login.component';
import { ManageIndexesComponent } from './manage-indexes/manage-indexes.component';
import { SelectSearchComponent } from './select-search/select-search.component';
import { SignupComponent } from './signup/signup.component';
import { StatewiseTrafficSourcesComponent } from './statewise-traffic-sources/statewise-traffic-sources.component';
import { TestSearchComponent } from './test-search/test-search.component';
import { TrafficSourcesComponent } from './traffic-sources/traffic-sources.component';
import { WordcloudComponent } from './wordcloud/wordcloud.component';

const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full'},
  { path: 'login', component: LoginComponent, canActivate:[AlreadyAuthServiceService] },
  { path: 'signup', component: SignupComponent, canActivate:[AlreadyAuthServiceService] },
  { path: 'home', component: HomeComponent, canActivate:[CheckAuthService] },
  { path: 'manage-indexes', component: HomeComponent, canActivate:[CheckAuthService] },
  { path: 'test-search', component: HomeComponent, canActivate:[CheckAuthService] },
  { path: 'select-search', component: HomeComponent, canActivate:[CheckAuthService] },
  { path: 'trafic-sources', component: HomeComponent, canActivate:[CheckAuthService] },
  { path: 'statewise-traffic', component: HomeComponent, canActivate:[CheckAuthService] },
  { path: 'analytics', component: HomeComponent, canActivate:[CheckAuthService] },
  { path: 'wordcloud', component: HomeComponent, canActivate:[CheckAuthService] },
  { path: 'live-logger', component: HomeComponent, canActivate:[CheckAuthService] },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
