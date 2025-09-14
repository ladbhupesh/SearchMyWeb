import { Component, OnInit } from '@angular/core';
import { Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { CellClickedEvent, ColDef } from 'ag-grid-community';
import { ToastrService } from 'ngx-toastr';
import { ApiServiceService } from '../api-service.service';
import { BooleanCellComponent } from '../boolean-cell/boolean-cell.component';

@Component({
  selector: 'app-list-all-urls',
  templateUrl: './list-all-urls.component.html',
  styleUrls: ['./list-all-urls.component.scss']
})
export class ListAllUrlsComponent implements OnInit {

  constructor(private api:ApiServiceService, private router: Router, private toastr:ToastrService) { }

  weblinks_data:any[] = [];

  column_names: ColDef[] = [
    { field: 'link_url', headerName: 'Link Url', resizable: true, filter:true },
    { field: 'index_level', headerName: 'Index Level', resizable: true, filter:true },
    { field: 'last_indexed_date', headerName: 'Last Indexed Date', resizable: true, filter:true },
    { field: 'is_indexed', headerName: 'Is Indexed', resizable: true, filter:true, cellRendererFramework:BooleanCellComponent },
    { field: 'to_be_crawled', headerName: 'To be Crawled', resizable: true, filter:true, cellRendererFramework:BooleanCellComponent }
  ];

  ngOnInit(): void {
    this.loadData() 
  }

  gridOptions = {
    onCellClicked: (event: CellClickedEvent) => {
      if (event.colDef.field=="link_url"){
        window.open(event.data.link_url, "_blank") 
      }
    },
    rowStyle: { cursor: 'pointer' },
    pagination: true,
  }
  
  loadData(){
    this.api.getAllWebLinks().subscribe(
      (response:any)=>{
        var tempList:any[] = []
        response.forEach(function(element:any){
          let index_level = element.index_level
          if(!element.index_level){
            index_level = "NA"
          }
          let last_indexed = element.last_indexed
          if(element.last_indexed){
            last_indexed = new Date(Date.parse(element.last_indexed)).toLocaleString()
          }
          tempList.push({
            link_url:element.link, 
            index_level:index_level,
            last_indexed_date:last_indexed,
            is_indexed:element.is_indexed,
            to_be_crawled:element.is_crawl,
          })
        });
        this.weblinks_data = tempList;
      },
      (error)=>{
      }
    )
  }

  startCrawlingLink(linkInput:HTMLInputElement){
    const reg = '(https?://)?([\\da-z.-]+)\\.([a-z.]{2,6})[/\\w .-]*/?';
    if(linkInput.validity.valid){
      this.api.startCrawlingUrl(linkInput.value).subscribe(
        (response:any)=>{
          if(response.status==200){
            this.toastr.info(response.message)
            this.toastr.success("Crawling starting");
            setInterval(this.loadData.bind(this),5000)
          }
          else{
            this.toastr.warning(response.message)
          }
        },
        (error)=>{
          this.toastr.error("Not able to start crawling");
        }
      )
    }else{
      this.toastr.warning("Please enter valid link");
    }
  }

}
