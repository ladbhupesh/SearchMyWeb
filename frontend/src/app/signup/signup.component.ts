import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { faEnvelope, faLock, faLongArrowAltRight, faUser } from '@fortawesome/free-solid-svg-icons';
import { ToastrService } from 'ngx-toastr';
import { ApiServiceService } from '../api-service.service';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.scss']
})
export class SignupComponent implements OnInit {

  constructor(private api:ApiServiceService,private router:Router, private toastr:ToastrService) { }

  fauser = faUser
  faenvelope = faEnvelope
  falongarrowaltright = faLongArrowAltRight
  faLock = faLock
  username:HTMLInputElement | undefined;
  email:HTMLInputElement | undefined;
  password:HTMLInputElement | undefined;
  password2:HTMLInputElement | undefined;

  ngOnInit(): void {
  }

  signup(username:HTMLInputElement,email:HTMLInputElement,password:HTMLInputElement,password2:HTMLInputElement){
    if(!email.validity.valid){
      this.toastr.warning("Please enter valid email.")
      return;
    }
    if(password.value != password2.value){
      this.toastr.warning("Both password should match.")
      return;
    }
    this.api.createUser(username.value,email.value,password.value,password2.value).subscribe(
      (response:any)=>{
        if(response.status_code == 200){
          this.toastr.success("User created successfully.")
          this.router.navigate(['/login'])
        }else{
          this.toastr.warning(response.status_message)
        }
      },
      (error)=>{
        this.toastr.warning("Internal server error.")
      }
    )
  }

}
