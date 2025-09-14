import {
  Injectable
} from '@angular/core';
import {
  ActivatedRouteSnapshot,
  CanActivate,
  Router,
  RouterStateSnapshot,
  UrlTree
} from '@angular/router';
import {
  map,
  Observable
} from 'rxjs';
import {
  ApiServiceService
} from './api-service.service';

@Injectable({
  providedIn: 'root'
})
export class CheckAuthService implements CanActivate {

  constructor(private router: Router, private api: ApiServiceService) {}

  canActivate(): Observable < boolean > | Promise < boolean > | boolean {
    return new Promise(res => {
      this.api.checkAuth().subscribe(
        (data:any) => {
          if (data.status_code == 200) {
            res(true);
          } else {
            this.router.navigate(['/login']);
            res(false);
          }
        },
        (error) => {
          this.router.navigate(['/login']);
          res(false);
        }
      );
    });
  }
}
