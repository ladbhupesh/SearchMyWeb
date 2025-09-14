import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { faBars,
  faGaugeHigh,
  faListCheck, 
  faMagnifyingGlass, 
  faHandPointer,
  faChartArea,
  faEarthAsia,
  faChartLine,
  faCloud,
  faFileLines,
  faRightFromBracket  
} from '@fortawesome/free-solid-svg-icons'
import { ApiServiceService } from '../api-service.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  constructor(private api:ApiServiceService, private router:Router) { }

  load_url = '/home';

  ngOnInit(): void {
    this.load_url = window.location.pathname
  }
  faBars = faBars;
  faGaugeHigh = faGaugeHigh;
  faListCheck = faListCheck; 
  faMagnifyingGlass = faMagnifyingGlass; 
  faHandPointer = faHandPointer;
  faChartArea = faChartArea;
  faEarthAsia = faEarthAsia;
  faChartLine = faChartLine;
  faCloud = faCloud;
  faFileLines = faFileLines;
  faRightFromBracket = faRightFromBracket;  
  is_active: boolean = false;
  toggleNavBar(){
      this.is_active = !this.is_active;       
  }

  check_path(path_name:string){
    if(path_name==this.load_url){
      return true;
    }
    return false;
  }

  logout(){
    this.api.deleteToken()
    window.location.href = "/login"
  }

}
