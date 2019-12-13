import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { ScoreService } from '../score.service';
@Component({
  selector: 'app-qp',
  templateUrl: './qp.component.html',
  styleUrls: ['./qp.component.css']
})
export class QPComponent implements OnInit {
  ans1 = new FormControl('');
  ans2 = new FormControl('');
  ans3 = new FormControl('');
  ans4 = new FormControl('');
  a;
  ans;
  marks = {};
  total = 0.0;
  constructor(public scoreservice: ScoreService) {
    this.ans = {1: '', 2: '', 3: '', 4: ''};
    this.marks = {'1': 0.0, '2': 0.0, '3': 0.0, '4': 0.0};
   }

  ngOnInit() {
  }
  extract() {
    this.a = {
      1: this.ans1.value,
      2: this.ans2.value,
      3: this.ans3.value,
      4: this.ans4.value
    };
    console.log(this.a);
    this.scoreservice.postData(this.a).subscribe(res => console.log(res));
  }
}
