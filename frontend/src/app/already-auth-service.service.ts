import {
  Injectable
} from '@angular/core';
import {
  CanActivate,
  Router
} from '@angular/router';
import {
  catchError,
  map,
  Observable
} from 'rxjs';
import {
  ApiServiceService
} from './api-service.service';

@Injectable({
  providedIn: 'root'
})
export class AlreadyAuthServiceService implements CanActivate {

  constructor(private router: Router, private api: ApiServiceService) {}

  canActivate(): Observable < boolean > | Promise < boolean > | boolean {
    return new Promise(res => {
      this.api.checkAuth().subscribe(
        (data:any) => {
          if (data.status_code == 200) {
            this.router.navigate(['']);
            res(false);
          } else {
            res(true);
          }
        },
        (error) => {
          res(true);
        }
      );
    });
  }
}
