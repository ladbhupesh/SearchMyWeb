import { Component, OnInit } from '@angular/core';
import { ApiServiceService } from '../api-service.service';

@Component({
  selector: 'app-test-search',
  templateUrl: './test-search.component.html',
  styleUrls: ['./test-search.component.scss']
})
export class TestSearchComponent implements OnInit {

  search_results_list:any[] = [];
  resultStatus = 'empty';

  constructor(private api:ApiServiceService) { }

  ngOnInit(): void {
  }

  search(queryInput:HTMLInputElement){
    this.resultStatus = 'loading';
    this.search_results_list = []
    this.api.getSearchResults(queryInput.value).subscribe(
      (response:any)=>{
        this.search_results_list = response.query_result;
        if(this.search_results_list.length==0){
          this.resultStatus = 'noresultfound';
        }
        else{
          this.resultStatus = 'empty';
        }
      },
      (error)=>{
        this.resultStatus = 'noresultfound';
        console.log(error)
      }
    )
  }

}
