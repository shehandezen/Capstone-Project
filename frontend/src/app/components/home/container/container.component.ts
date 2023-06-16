import {
  Component,
  ViewChild,
  ElementRef,
  OnDestroy,
  OnChanges,
} from '@angular/core';

@Component({
  selector: 'app-container',
  templateUrl: './container.component.html',
  styleUrls: ['./container.component.css'],
})
export class ContainerComponent {
  @ViewChild('hero', { static: true }) hero: ElementRef;
  @ViewChild('formToggle', { static: true }) formToggle: ElementRef;
  // @ViewChild('SignIn') signIn: ElementRef;
  // @ViewChild('SignUp') signUp: ElementRef;
  toggle = true;

  toggleForms() {
    if (this.toggle) {
      this.formToggle.nativeElement.textContent = 'Sign up';
      // this.signUp.nativeElement.style.display = 'none';
      // this.hero.nativeElement.style.top = '0px';
    } else {
      this.formToggle.nativeElement.textContent = 'Sign in';
      // this.signIn.nativeElement.style.display = 'none';
      // this.hero.nativeElement.style.top = '0px';
    }
    this.toggle = !this.toggle;
  }
}
