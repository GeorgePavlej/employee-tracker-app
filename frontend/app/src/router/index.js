import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import MainLayout from '../components/layout/MainLayout.vue'
import ClockInOut from '../components/statements/ClockInOut.vue'
import LogsView from '../components/statements/LogsView.vue'
import ShiftsView from '../components/statements/ShiftsView.vue'
import ReportsView from '../components/statements/ReportsView.vue'
import LeaveManagementView from '../components/statements/LeaveManagementView.vue'
import EmployeeManagementView from '../components/statements/EmployeeManagementView.vue'
import { isAuthenticated } from '../utils/auth'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/section/:section',
    redirect: to => {
      const sectionMap = {
        'clockInOut': 'clockInOut',
        'logs': 'logs',
        'shifts': 'shifts',
        'reports': 'reports',
        'leaveManagement': 'leaveManagement',
        'employeeManagement': 'employeeManagement'
      };
      
      const targetRoute = sectionMap[to.params.section] || 'dashboard';
      return { name: targetRoute };
    }
  },
  {
    path: '/dashboard',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'dashboard',
        component: ClockInOut
      },
      {
        path: 'clock-in-out',
        name: 'clockInOut',
        component: ClockInOut
      },
      {
        path: 'logs',
        name: 'logs',
        component: LogsView
      },
      {
        path: 'shifts',
        name: 'shifts',
        component: ShiftsView
      },
      {
        path: 'reports',
        name: 'reports',
        component: ReportsView
      },
      {
        path: 'leave-management',
        name: 'leaveManagement',
        component: LeaveManagementView
      },
      {
        path: 'employee-management',
        name: 'employeeManagement',
        component: EmployeeManagementView
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory('/'),
  routes
})

router.beforeEach((to, from, next) => {
  const isAuth = isAuthenticated()
  
  if ((to.path === '/' || to.path === '/dashboard') && !isAuth) {
    next({ name: 'login' });
    return;
  }
  
  if (to.matched.some(record => record.meta.requiresAuth) && !isAuth) {
    next({ name: 'login' })
  } else if (to.path === '/login' && isAuth) {
    next({ name: 'dashboard' })
  } else {
    next()
  }
})

export default router
