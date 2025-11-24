import { Component } from "@angular/core";
import { Topbar } from "../topbar/topbar.component";
import { Footer } from "../footer/footer.component";

@Component({
    standalone:true,
    selector:'app-home',
    templateUrl:'./home.component.html',
    styleUrl:'./home.component.scss',
    imports:[Topbar, Footer]
})
export class Home {}