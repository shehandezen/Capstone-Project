import {
  Component,
  Input,
  ViewChild,
  OnChanges,
  OnDestroy,
  ElementRef,
} from '@angular/core';

@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.css'],
})
export class SignInComponent implements OnChanges {
  @Input() toggle: boolean;

  @ViewChild('signIn') signIn: ElementRef;

  ngOnChanges() {
    // if (this.toggle) {
    //   this.signIn.nativeElement.style.display = 'none';
    // } else {
    //   this.signIn.nativeElement.style.display = 'flex';
  }

  // console.log(this.toggle);
}
