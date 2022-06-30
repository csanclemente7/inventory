import { createRouter, createWebHistory } from "vue-router";
import App from "./App.vue";
import LogIn from "./components/LogIn.vue";
import Home from "./components/Home.vue";
import Input from "./components/Input.vue";
const routes = [
  {
    path: "/",
    name: "root",
    component: App,
  },
  {
    path: "/logIn",
    name: "logIn",
    component: LogIn,
  },
  {
    path: "/home",
    name: "home",
    component: Home,
  },
  {
    path: "/input",
    name: "input",
    component: Input,
  },
];
const router = createRouter({
  history: createWebHistory(),
  routes,
});
export default router;
