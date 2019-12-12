import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
@Injectable({
  providedIn: 'root'
})
export class ScoreService {

  constructor(private http: HttpClient) { }

  getScore() {
    return this.http.get(environment.score_url);
  }
  postData(data: any) {
    console.log('serv ' + data);
    return this.http.post(environment.score_url, data);
  }
}
