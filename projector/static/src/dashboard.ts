import { MDCDrawer } from "@material/drawer";
import { MDCTopAppBar } from "@material/top-app-bar";
import { MDCList } from "@material/list";
import "./dashboard.scss";

const drawer = MDCDrawer.attachTo(document.querySelector(".mdc-drawer")!);
const topAppBarElement = document.querySelector(".mdc-top-app-bar")!;
const topAppBar = new MDCTopAppBar(topAppBarElement);
const list = new MDCList(document.querySelector(".mdc-list")!);

const listEl = document.querySelector(".mdc-drawer .mdc-list")!;
const mainContentEl = document.querySelector(".main-content")!;

listEl.addEventListener("click", (event) => {
  mainContentEl.querySelector("input, button")!.focus();
});

topAppBar.listen("MDCTopAppBar:nav", () => {
  drawer.open = !drawer.open;
});
