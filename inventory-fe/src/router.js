import { createRouter, createWebHistory } from "vue-router";
import App from "./App.vue";
import LogIn from "./components/LogIn.vue";
import SignUp from "./components/SignUp.vue";
import Home from "./components/Home.vue";
import Historial from "./components/Historial.vue";
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
    path: "/signUp",
    name: "signUp",
    component: SignUp,
  },
  {
    path: "/home",
    name: "home",
    component: Home,
  },
  {
    path: "/historial",
    name: "historial",
    component: Historial,
  },
];
const router = createRouter({
  history: createWebHistory(),
  routes,
});
export default router;
