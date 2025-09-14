import { Component, OnInit } from '@angular/core';
import { ApiServiceService } from '../api-service.service';

@Component({
  selector: 'app-livelogger',
  templateUrl: './livelogger.component.html',
  styleUrls: ['./livelogger.component.scss']
})
export class LiveloggerComponent implements OnInit {

  constructor(private api: ApiServiceService) { }

  logger_list:string[] = []

  ngOnInit(): void {
    this.loadLogger()
    setInterval(this.loadLogger.bind(this),2000)
  }

  loadLogger(){
    this.api.getLiveLogger().subscribe(
      (response:any)=>{
        this.logger_list = response
      let element = document.getElementById("logger-div")
      if(element && element.scrollHeight){
        element.scrollTop = element.scrollHeight
      }
      },
      (error)=>{
        console.log(error);
      }
    )
  }

}
