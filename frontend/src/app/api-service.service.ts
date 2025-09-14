import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiServiceService {

  private apiToken:any = ''
  constructor(
    private http: HttpClient,
    private router:Router
  ) { this.apiToken = this.getLocalToken() }

  setToken(token:string){
    localStorage.setItem("token",token)
  }

  getLocalToken(){
    var token = localStorage.getItem("token")
    return token
  }

  deleteToken(){
    localStorage.removeItem("token")
  }

  isValidTonen(): Observable < boolean > | Promise < boolean > | boolean{
    return new Promise(res => {
      this.checkAuth().subscribe(
        (data:any) => {
          if (data.status_code == 200) {
            res(true);
          } else {
            this.router.navigate(['/login']);
            res(false);
          }
        },
        (error) => {
          this.router.navigate(['/login']);
          res(false);
        }
      );
    });
  }

  checkAuth(){
    var header = new HttpHeaders({AUTHTOKEN: this.apiToken})
    return this.http.get(`${environment.API_URL}/check-auth`,{headers: header})
  }

  getToken(username:string,password:string){
    return this.http.post(`${environment.API_URL}/login`,{username:username,password:password})
  }

  createUser(username:string,email:string,password:string,password2:string){
    return this.http.post(`${environment.API_URL}/signup`,{username:username,email:email,password1:password,password2:password2})
  }

  getAllWebLinks(){
    var header = new HttpHeaders({AUTHTOKEN: this.apiToken})
    return this.http.get(`${environment.API_URL}/get-all-web-links`,{headers: header})
  }

  getManageIndexesList(){
    var header = new HttpHeaders({AUTHTOKEN: this.apiToken})
    return this.http.get(`${environment.API_URL}/get-manage-indexes-list`,{headers: header})
  }

  deleteIndex(id:number){
    var header = new HttpHeaders({AUTHTOKEN: this.apiToken})
    return this.http.delete(`${environment.API_URL}/manage-index/${id}`,{headers: header})
  }

  updateIndex(id:number){
    var header = new HttpHeaders({AUTHTOKEN: this.apiToken})
    return this.http.put(`${environment.API_URL}/manage-index/${id}`,{},{headers: header})
  }

  getTraficSourcesList(){
    var header = new HttpHeaders({AUTHTOKEN: this.apiToken})
    return this.http.get(`${environment.API_URL}/get-trafic-sources-list`,{headers: header})
  }

  getStateWiseTrafic(startDate:string,endDate:string){
    var header = new HttpHeaders({AUTHTOKEN: this.apiToken})
    let query = `?start_date=${startDate}&end_date=${endDate}`
    return this.http.get(`${environment.API_URL}/get-state-wise-traffic${query}`,{headers: header})
  }

  getAnalyticsDetails(startDate:string,endDate:string){
    var header = new HttpHeaders({AUTHTOKEN: this.apiToken})
    let query = `?start_date=${startDate}&end_date=${endDate}`
    return this.http.get(`${environment.API_URL}/analytics-details${query}`,{headers: header})
  }

  getWordCloudDetails(startDate:string,endDate:string){
    var header = new HttpHeaders({AUTHTOKEN: this.apiToken})
    let query = `?start_date=${startDate}&end_date=${endDate}`
    return this.http.get(`${environment.API_URL}/wordcloud-details${query}`,{headers: header})
  }

  getLiveLogger(){
    var header = new HttpHeaders({AUTHTOKEN: this.apiToken})
    return this.http.get(`${environment.API_URL}/get-live-logger`,{headers: header})
  }

  getSearchResults(query:string){
    var header = new HttpHeaders({AUTHTOKEN: this.apiToken})
    return this.http.get(`${environment.API_URL}/search/${query}`,{headers: header})
  }

  getDeployLink(){
    var header = new HttpHeaders({AUTHTOKEN: this.apiToken})
    return this.http.get(`${environment.API_URL}/select-search`,{headers: header})
  }

  startCrawlingUrl(url:string){
    var header = new HttpHeaders({AUTHTOKEN: this.apiToken})
    return this.http.post(`${environment.API_URL}/start-crawling`,{url:url},{headers: header})
  }
}
