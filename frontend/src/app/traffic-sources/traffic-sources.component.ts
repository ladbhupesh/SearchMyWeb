import { Component, OnInit } from '@angular/core';
import { CellClickedEvent, ColDef } from 'ag-grid-community';
import { ApiServiceService } from '../api-service.service';

@Component({
  selector: 'app-traffic-sources',
  templateUrl: './traffic-sources.component.html',
  styleUrls: ['./traffic-sources.component.scss']
})
export class TrafficSourcesComponent implements OnInit {

  constructor(private api:ApiServiceService) { }

  weblinks_data:any[] = [];

  column_names: ColDef[] = [
    { field: 'link_url', headerName: 'Link Url', resizable: true, filter:true, width:600 },
    { field: 'click_count', headerName: 'Click Count', resizable: true, filter:true },
    { field: 'last_indexed_date', headerName: 'Last Indexed Date', resizable: true, filter:true },
  ];

  ngOnInit(): void {
    this.getData()
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

  getData(){
    this.api.getTraficSourcesList().subscribe(
      (response:any)=>{
        var tempList:any[] = []
        response.forEach(function(element:any){
          let last_indexed = element.last_indexed
          if(element.last_indexed){
            last_indexed = new Date(Date.parse(element.last_indexed)).toLocaleString()
          }
          tempList.push({
            link_url:element.link,
            click_count:element.click_count,
            last_indexed_date:last_indexed,
          })
        });
        this.weblinks_data = tempList;
      },
      (error)=>{console.log(error)}
    )
  }

}
