import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ContainerComponent } from './components/home/container/container.component';
import { SignInComponent } from './components/home/sign-in/sign-in.component';
import { SignUpComponent } from './components/home/sign-up/sign-up.component';
import { LoaderComponent } from './components/loader/loader.component';
import { SidebarComponent } from './components/dashboard/sidebar/sidebar.component';
import { HeaderComponent } from './components/dashboard/header/header.component';
import { DashboardContainerComponent } from './components/dashboard/dashboard-container/dashboard-container.component';
import { MainComponent } from './components/dashboard/main/main.component';
import { CardSectionComponent } from './components/dashboard/workspace/card-section/card-section.component';
import { AdminComponent } from './components/dashboard/workspace/admin/admin/admin.component';
import { AdminTableComponent } from './components/dashboard/workspace/admin/admin-table/admin-table.component';
import { AdminProfileComponent } from './components/dashboard/workspace/admin/admin-profile/admin-profile.component';
import { TeacherComponent } from './components/dashboard/workspace/teacher/teacher/teacher.component';
import { TeacherTableComponent } from './components/dashboard/workspace/teacher/teacher-table/teacher-table.component';
import { TeacherProfileComponent } from './components/dashboard/workspace/teacher/teacher-profile/teacher-profile.component';
import { StudentComponent } from './components/dashboard/workspace/student/student/student.component';
import { StudentTableComponent } from './components/dashboard/workspace/student/student-table/student-table.component';
import { StudentProfileComponent } from './components/dashboard/workspace/student/student-profile/student-profile.component';
import { CourseComponent } from './components/dashboard/workspace/course/course/course.component';
import { CourseDetailsComponent } from './components/dashboard/workspace/course/course-details/course-details.component';
import { CourseTableComponent } from './components/dashboard/workspace/course/course-table/course-table.component';
import { CourseCreateComponent } from './components/dashboard/workspace/course/course-create/course-create.component';
import { GradeComponent } from './components/dashboard/workspace/grade/grade.component';
import { AttendanceComponent } from './components/dashboard/workspace/attendance/attendance.component';

@NgModule({
  declarations: [
    AppComponent,
    ContainerComponent,
    SignInComponent,
    SignUpComponent,
    LoaderComponent,
    SidebarComponent,
    HeaderComponent,
    DashboardContainerComponent,
    MainComponent,
    CardSectionComponent,
    AdminComponent,
    AdminTableComponent,
    AdminProfileComponent,
    TeacherComponent,
    TeacherTableComponent,
    TeacherProfileComponent,
    StudentComponent,
    StudentTableComponent,
    StudentProfileComponent,
    CourseComponent,
    CourseDetailsComponent,
    CourseTableComponent,
    CourseCreateComponent,
    GradeComponent,
    AttendanceComponent,
  ],
  imports: [BrowserModule, AppRoutingModule],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
