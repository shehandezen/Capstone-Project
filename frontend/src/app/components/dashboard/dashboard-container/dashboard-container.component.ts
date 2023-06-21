import { Component, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-dashboard-container',
  templateUrl: './dashboard-container.component.html',
  styleUrls: ['./dashboard-container.component.css'],
})
export class DashboardContainerComponent {
  sideBarToggled: boolean = true;

  onToggle(value: boolean) {
    this.sideBarToggled = value;
  }
}
