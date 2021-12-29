import Vue from 'vue'
import VueRouter from 'vue-router'
import Welcome from '../views/Welcome.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Welcome',
    component: Welcome
  },
  {
    path: '/labelspace',
    name: 'LabelSpace',
    component: () => import('../views/LabelSpace.vue')
  },
  { path: '/groupview',
    name: 'Groupview',
    component: () => import('../views/Groupview.vue')
  },
  { path: '/overview',
    name: 'Overview',
    component: () => import('../views/Overview.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
