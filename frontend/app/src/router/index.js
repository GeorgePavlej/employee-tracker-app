import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import Statements from '../views/Statements.vue'
import { isAuthenticated } from '../utils/auth'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/statements',
    name: 'statements',
    component: Statements,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory('/'),
  routes
})

router.beforeEach((to, from, next) => {
  const isAuth = isAuthenticated()
  
  if ((to.path === '/' || to.path === '/statements') && !isAuth) {
    next({ name: 'login' });
    return;
  }
  
  if (to.matched.some(record => record.meta.requiresAuth) && !isAuth) {
    next({ name: 'login' })
  } else if (to.path === '/login' && isAuth) {
    next({ name: 'statements' })
  } else {
    next()
  }
})

export default router

