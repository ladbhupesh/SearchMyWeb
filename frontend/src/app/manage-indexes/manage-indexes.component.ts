import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CellClickedEvent, ColDef } from 'ag-grid-community';
import { ApiServiceService } from '../api-service.service';
import { BooleanCellComponent } from '../boolean-cell/boolean-cell.component';
import { DeleteCellComponent } from '../delete-cell/delete-cell.component';
import { UpdateCellComponent } from '../update-cell/update-cell.component';

@Component({
  selector: 'app-manage-indexes',
  templateUrl: './manage-indexes.component.html',
  styleUrls: ['./manage-indexes.component.scss']
})
export class ManageIndexesComponent implements OnInit {

  constructor(private api:ApiServiceService, private router: Router) { }

  weblinks_data:any[] = [];

  column_names: ColDef[] = [
    { field: 'link_url', headerName: 'Link Url', resizable: true, filter:true, width:400 },
    { field: 'last_indexed_date', headerName: 'Last Indexed Date', resizable: true, filter:true },
    { field: 'update', headerName: 'Update', resizable: true, filter:true, cellRendererFramework:UpdateCellComponent },
    { field: 'delete', headerName: 'Delete', resizable: true, filter:true, cellRendererFramework:DeleteCellComponent }
  ];

  ngOnInit(): void {
    this.getData()
  }

  gridOptions = {
    onCellClicked: (event: CellClickedEvent) => {
      if (event.colDef.field=="link_url"){
        window.open(event.data.link_url, "_blank") 
      }
      if (event.colDef.field=="delete"){
        console.log(event.data.delete)
        this.api.deleteIndex(event.data.delete).subscribe(
          (ressponse:any)=>{
            if(ressponse.status == 200){
              this.getData()
            }
          },
          (error)=>{console.log(error)}
        )
      }
    },
    rowStyle: { cursor: 'pointer' },
    pagination: true,
  }

  getData(){
    this.api.getManageIndexesList().subscribe(
      (response:any)=>{
        var tempList:any[] = []
        response.forEach(function(element:any){
          let last_indexed = element.last_indexed
          if(element.last_indexed){
            last_indexed = new Date(Date.parse(element.last_indexed)).toLocaleString()
          }
          tempList.push({
            link_url:element.link,
            last_indexed_date:last_indexed,
            update:element.id,
            delete:element.id,
          })
        });
        this.weblinks_data = tempList;
      },
      (error)=>{
      }
    )
  }

}
