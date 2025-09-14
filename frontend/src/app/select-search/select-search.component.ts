import { Component, OnInit, Renderer2 } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { ApiServiceService } from '../api-service.service';
import { EnjectJsService } from '../enject-js.service';

@Component({
  selector: 'app-select-search',
  templateUrl: './select-search.component.html',
  styleUrls: ['./select-search.component.scss']
})
export class SelectSearchComponent implements OnInit {

  constructor(private api:ApiServiceService, private toastr:ToastrService, private enject:EnjectJsService, private renderer:Renderer2) { }

  declare checkSelectedText:any
  deplot_link = ''

  ngOnInit(): void {
    this.api.getDeployLink().subscribe(
      (response:any)=>{
        if(response.status_code==200){
          this.deplot_link = response.deploy_js_link
          const scriptElement = this.enject.loadJsScript(this.renderer,this.deplot_link)
          scriptElement.onload=()=>{
            this.toastr.success("Select Search script loaded successfully.");
          }
          scriptElement.onerror=()=>{
            this.toastr.error("Unable loaded select Search script.");
          }
        }
        else{
          this.toastr.error(response.status_message)
        }
      },
      (error)=>{
        this.toastr.error(error)
      }
    )
  }

  copyInputMessage(inputElement:HTMLInputElement){
    inputElement.select();
    document.execCommand('copy');
    inputElement.setSelectionRange(0, 0);
  }

}
