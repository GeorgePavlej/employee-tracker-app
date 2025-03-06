import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import Statements from '../views/Statements.vue'

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

// Navigation guard to check authentication
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('auth') !== null
  
  // If root path or statements, check authentication first
  if ((to.path === '/' || to.path === '/statements') && !isAuthenticated) {
    next({ name: 'login' });
    return;
  }
  
  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    // If the route requires auth and user is not authenticated, redirect to login
    next({ name: 'login' })
  } else if (to.path === '/login' && isAuthenticated) {
    // If user is already authenticated and tries to access login, redirect to statements
    next({ name: 'statements' })
  } else {
    next()
  }
})

export default router

