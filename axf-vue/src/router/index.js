import Vue from 'vue'
import Router from 'vue-router'

import Home from '@/components/Home'
import Market from '@/components/Market'
import Cart from '@/components/Cart'
import Mine from '@/components/Mine'

import Rigister from '@/components/register'
import Login from '@/components/login'
import Orders from '@/components/OrderList'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/home',
      name: 'Home',
      component: Home,
    },
    {
      path: '/market',
      name: 'Market',
      component: Market
    },
    {
      path: '/cart',
      name: 'Cart',
      component: Cart
    },
    {
      path: '/mine',
      name: 'Mine',
      component: Mine,
    },
    {
      path:'/register',
      name:'register',
      component: Rigister
    },
    {
      path:'/login',
      name:'login',
      component: Login
    },
    {
      path:'/',
      redirect: '/home'
    },
    {
      path: '/orders',
      component: Orders
    }
  ]
})
