import { Component, OnInit } from '@angular/core';
import { faArrowsRotate } from '@fortawesome/free-solid-svg-icons';
import { ApiServiceService } from '../api-service.service';
import {
  trigger,
  state,
  style,
  animate,
  transition
} from '@angular/animations';

@Component({
  selector: 'app-update-cell',
  templateUrl: './update-cell.component.html',
  styleUrls: ['./update-cell.component.scss'],
  animations: [
    trigger('rotatedState', [
      state('default', style({ transform: 'rotate(0)' })),
      state('rotated', style({ transform: 'rotate(-360deg)' })),
      transition('rotated => default', animate('2000ms ease-out')),
      transition('default => rotated', animate('2000ms ease-in'))
    ])
  ],
})
export class UpdateCellComponent implements OnInit {


  data:any;
  faBooleanIcon = faArrowsRotate;
  state = false
  color = 'gray'
  constructor(private api:ApiServiceService) { 

  }

  agInit(params:any){
    this.data = params
  }

  ngOnInit(): void {
  }

  updateLink(){
    this.state = true
    this.api.updateIndex(this.data.value).subscribe(
      (ressponse:any)=>{
        if(ressponse.status == 200){
          this.state = false
        }
      },
      (error)=>{console.log(error)}
    )
  }

}
