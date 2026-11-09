import { createRouter, createWebHistory } from "vue-router"
import Home from "../pages/Home.vue"
import AppPage from "../pages/AppPage.vue"
import ResultPage from "../pages/Resultpage.vue"
import Detail from '../pages/Detail.vue'
import History from "../pages/History.vue"

const routes = [
  { path: "/", component: Home },
  { path: "/features", component: AppPage },
  { path: "/results", name: "ResultPage", component: ResultPage },
  { path: "/detail", name: 'Detail', component: Detail },
  { path: "/history", component: History },  
]

export default createRouter({
  history: createWebHistory(),
  routes
})
