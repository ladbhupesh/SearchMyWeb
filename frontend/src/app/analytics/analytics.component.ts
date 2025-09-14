import { Component, OnInit } from '@angular/core';
import { Chart } from 'chart.js';
import { ToastrService } from 'ngx-toastr';
import { ApiServiceService } from '../api-service.service';

@Component({
  selector: 'app-analytics',
  templateUrl: './analytics.component.html',
  styleUrls: ['./analytics.component.scss']
})
export class AnalyticsComponent implements OnInit {

  constructor(private api:ApiServiceService, private toastr:ToastrService) { }

  ngOnInit(){
    this.loadData("","")
  }

  date_labels:any[] = [];
  total_click_count_list:any[] = [];
  total_search_count_list:any[] = [];

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
    this.loadData(startDate.value,endDate.value)
  }

  loadData(startDate:string,endDate:string){
    let temp_date_labels:any[] = []
    let temp_total_click_count_list:any[] = []
    let temp_total_search_count_list:any[] = []
    this.api.getAnalyticsDetails(startDate,endDate).subscribe(
      (response:any) =>{
        response.forEach(function(element:any){
          temp_date_labels.push(element.created_date)
          temp_total_click_count_list.push(element.total_click_count)
          temp_total_search_count_list.push(element.total_search_count)
        });
        this.date_labels = temp_date_labels;
        this.total_click_count_list = temp_total_click_count_list;
        this.total_search_count_list = temp_total_search_count_list;
        var myChart = new Chart("analytics-chart", {
          type: "line",
          data: {
              labels: this.date_labels,
              datasets: [
                  {
                      label:"Click Count",
                      borderColor: "red",
                      data: this.total_click_count_list
                  },
                  {
                      label:"Search Count",
                      borderColor: "green",
                      data: this.total_search_count_list
                  }
              ]
          },
          options: {
              scales: {
                  yAxes: [{
                      ticks: {
                          beginAtZero: true
                      }
                  }]
              }
          }
        });
        this.toastr.success("Data loaded successfully.")
      },
      (error)=>{
        this.toastr.error("Unable to load data.")
        console.log(error)
      }
    )
  }
}
