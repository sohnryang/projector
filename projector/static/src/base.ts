import { MDCDrawer } from "@material/drawer";
import { MDCTopAppBar } from "@material/top-app-bar";
import { MDCDataTable } from "@material/data-table";
import { MDCMenu } from "@material/menu";

import "./base.scss";

const drawer = MDCDrawer.attachTo(document.querySelector(".mdc-drawer")!);
const topAppBarElement = document.querySelector(".mdc-top-app-bar")!;
const topAppBar = new MDCTopAppBar(topAppBarElement);
const dataTable = new MDCDataTable(document.querySelector("#post-list")!);

const listEl = document.querySelector(".mdc-drawer .mdc-list")!;
const mainContentEl = document.querySelector(".main-content")!;
const menuElem = document.querySelector("#account-menu")!;
const menu = new MDCMenu(menuElem);
menu.open = false;
menu.listen("MDCMenu:selected", (event) => {
  console.log(event);
});

topAppBar.listen("MDCTopAppBar:nav", () => {
  drawer.open = !drawer.open;
});

const accountButtonElem = document.querySelector("#account-button")!;
accountButtonElem.addEventListener("click", () => {
  menu.open = !menu.open;
});
