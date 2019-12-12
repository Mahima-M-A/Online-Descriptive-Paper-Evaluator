import { Component, OnInit } from '@angular/core';
import { ScoreService } from '../score.service';
@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent implements OnInit {
  marks;
  total = 0.0;
  constructor(public scoreservice: ScoreService) {
    this.calculate();
  }
  ngOnInit() {
  }
  calculate() {
    this.marks = {'1': 0.0,'2': 0.0,'3': 0.0,'4': 0.0};
    this.scoreservice.getScore().subscribe((data: any) => {
      for (const key in data) {
        if (data.hasOwnProperty(key)) {
          this.marks[key] = parseFloat(data[key]).toFixed(2);
          console.log(this.marks[key]);
          this.total += parseFloat(this.marks[key]);
          console.log(this.total.toFixed(2));
        }
      }
    });
  }
}
