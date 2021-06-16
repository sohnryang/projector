import { MDCDrawer } from "@material/drawer";
import { MDCTopAppBar } from "@material/top-app-bar";
import { MDCDataTable } from "@material/data-table";
import "./dashboard.scss";

const drawer = MDCDrawer.attachTo(document.querySelector(".mdc-drawer")!);
const topAppBarElement = document.querySelector(".mdc-top-app-bar")!;
const topAppBar = new MDCTopAppBar(topAppBarElement);
const dataTable = new MDCDataTable(document.querySelector(".mdc-data-table")!);

const listEl = document.querySelector(".mdc-drawer .mdc-list")!;
const mainContentEl = document.querySelector(".main-content")!;

listEl.addEventListener("click", (event) => {
  mainContentEl.querySelector("input, button")!.focus();
});

topAppBar.listen("MDCTopAppBar:nav", () => {
  drawer.open = !drawer.open;
});
