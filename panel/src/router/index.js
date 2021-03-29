import Vue from 'vue'
import VueRouter from 'vue-router'
import ViewData from '../views/ViewData.vue'
import Stat from '../views/Stat.vue'
import Welcome from '../views/Welcome.vue'
import WordCloud from '../views/WordCloud.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Welcome',
    component: Welcome
  },
  {
    path: '/viewdata',
    name: 'ViewData',
    component: ViewData
  },
  {
    path: '/stat',
    name: 'Stat',
    component: Stat
  },
  {
    path: '/wordcloud',
    name: 'WordCloud',
    component: WordCloud
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
