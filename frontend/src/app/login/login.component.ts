import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { faUser,faEnvelope,faLongArrowAltRight,faLock } from '@fortawesome/free-solid-svg-icons'
import { ToastrService } from 'ngx-toastr';
import { ApiServiceService } from '../api-service.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  constructor(private api:ApiServiceService,private router:Router, private toastr:ToastrService) { }

  fauser = faUser
  faenvelope = faEnvelope
  falongarrowaltright = faLongArrowAltRight
  faLock = faLock
  username:HTMLInputElement | undefined;
  password:HTMLInputElement | undefined;
  errors:{haserror:boolean,error:string} = {haserror:false,error:""}
  ngOnInit(): void {
  }

  login(username:HTMLInputElement,password:HTMLInputElement){
    this.username = username;
    this.password = password;
    this.errors.haserror = false
    this.errors.error = ""
    if(username.value=="" || password.value ==""){
      this.toastr.warning("All fields required")
      return          
    }

    this.api.getToken(username.value,password.value).subscribe(
      (response:any) =>{
        if(response.status_code==200){
          this.api.setToken(response.auth_token)
          setTimeout(this.toHome.bind(this),500)    
        }
        else{
          setTimeout(this.showErrors.bind(this),2000)
        }
      },
      (error) =>{
        setTimeout(this.showErrors.bind(this),2000)
        console.log(error);
      }
    )
  }

  showErrors(){
      this.toastr.error("InValid username password")

      if(this.username){
        this.username.value = "";
      }
      if(this.password){
        this.password.value = "";
      }
      return                
  }

  toHome(){
    this.toastr.success("Login successfully")
    window.location.reload();
  }
}
