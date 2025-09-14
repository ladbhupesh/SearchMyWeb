import { Component, OnInit } from '@angular/core';
import { faTrash } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-delete-cell',
  templateUrl: './delete-cell.component.html',
  styleUrls: ['./delete-cell.component.scss']
})
export class DeleteCellComponent implements OnInit {

  
  data:any;
  faTrash = faTrash;
  color = 'red'
  mouseHovar = false;
  constructor() { 

  }

  agInit(params:any){
    this.data = params
  }

  deleteLink(){
  }

  ngOnInit(): void {
  }

}
