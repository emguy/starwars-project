import Vue from 'vue'
import Router from 'vue-router'
import Main from '@/views/Main'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: '/myapp',
  routes: [
    {
      path: '/',
      name: 'Main',
      component: Main
    }
  ]
})
