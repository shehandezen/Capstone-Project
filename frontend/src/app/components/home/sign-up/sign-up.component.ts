import {
  Component,
  Input,
  OnChanges,
  ViewChild,
  ElementRef,
} from '@angular/core';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css'],
})
export class SignUpComponent {
  @Input() toggle: boolean;
  @ViewChild('signUp') signUp: ElementRef;

  ngOnChanges() {
    // if (this.toggle) {
    //   this.signUp.nativeElement.style.display = 'flex';
    // } else {
    //   this.signUp.nativeElement.style.display = 'none';
    // }

    console.log(this.toggle);
  }
}
