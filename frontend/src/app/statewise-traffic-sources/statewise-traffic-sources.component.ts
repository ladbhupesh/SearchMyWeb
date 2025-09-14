import {
  Component,
  OnInit
} from '@angular/core';
import { Router } from '@angular/router';
import {
  end, right
} from '@popperjs/core';
import { ToastrService } from 'ngx-toastr';
import { ApiServiceService } from '../api-service.service';

@Component({
  selector: 'app-statewise-traffic-sources',
  templateUrl: './statewise-traffic-sources.component.html',
  styleUrls: ['./statewise-traffic-sources.component.scss']
})
export class StatewiseTrafficSourcesComponent implements OnInit {

  constructor(private api: ApiServiceService, private router:Router, private toastr:ToastrService) {}

  state_wise_count = []
  choose_state = "Choose State"

  ngOnInit(): void {
    document.querySelectorAll('.state-path').forEach(element=>{
      element.setAttribute("style","stroke: #000000;stroke-width: 1px;stroke-linejoin: round;cursor: pointer;fill:"+this.getRandomColor()) 
    })
    if(this.api.isValidTonen()){
      this.loadData("","")
    }
    else{
      this.router.navigate(['/login'])
    }
  }

  colorArray:string[] = []

  applyFilter(startDate: HTMLInputElement, endDate: HTMLInputElement) {
    if (startDate.value == '' || endDate.value == '') {
      // alert("Both Dates Required")
      this.toastr.warning("Both Dates Required")
      return;
    }
    if (new Date(startDate.value) > new Date(endDate.value)) {
      // alert("Start Date must be smaller that end date")
      this.toastr.warning("Start Date must be smaller that end date")
      return;
    }
    if(this.api.isValidTonen()){
      this.loadData(startDate.value,endDate.value)
    }
    else{
      this.router.navigate(['/login'])
    }
  }

  loadData(startDate:string,endDate:string){
    document.querySelectorAll('.state-path').forEach(element=>{
      element.setAttribute("data-count","0") 
    })
    this.api.getStateWiseTrafic(startDate,endDate).subscribe(
      (response:any) =>{
        response.forEach(function(element:any){
          let state_wise_count_list = JSON.parse(element.state_wise_count)
          state_wise_count_list.forEach(function(state_elemet:any){
            let elm = document.querySelector('.state-path[title="'+state_elemet.state+'"]')
            let existing_count = elm?.getAttribute("data-count")

            let count:number = 0
            if (existing_count){
              count = parseInt(existing_count)
            }
            
            elm?.setAttribute("data-count",(count+state_elemet.frequency).toString())
          });
        });
        this.toastr.success("Data loaded succefully")
      },
      (error)=>{
        this.toastr.error("Error while loading data")
        console.log(error)
      }
    )
  }

  getRandomColor():string {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    if(this.colorArray.includes(color)){
        return this.getRandomColor();
    }
    this.colorArray.push(color)
    return color;
  }

  mouseEnter(event:any){
    this.choose_state = event.target.getAttribute("title") + " : " + event.target.getAttribute("data-count")
    // console.log(event.target)
  }
  mouseLeave(event:any){
    this.choose_state = "Choose State"
  }
}
