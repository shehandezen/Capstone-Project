import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css'],
})
export class MainComponent {
  @Input() sideBarToggled: boolean;
  @Output() toggle = new EventEmitter<boolean>();

  onToggle(value: boolean) {
    this.toggleEvent(value);
  }
  toggleEvent(value: boolean) {
    this.sideBarToggled = value;
    this.toggle.emit(this.sideBarToggled);
  }
}
