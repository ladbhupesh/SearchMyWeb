import { Component, OnInit } from '@angular/core';
import { faCircleCheck,faXmarkCircle } from '@fortawesome/free-solid-svg-icons'

@Component({
  selector: 'app-boolean-cell',
  templateUrl: './boolean-cell.component.html',
  styleUrls: ['./boolean-cell.component.scss']
})
export class BooleanCellComponent implements OnInit {

  data:any;
  faBooleanIcon = faXmarkCircle;
  color = 'red'
  constructor() { 

  }

  agInit(params:any){
    this.data = params.value
    if(this.data){
      this.faBooleanIcon = faCircleCheck;
      this.color = 'green'
    }
  }

  ngOnInit(): void {
  }

}
