import Vue from 'vue'
import VueRouter from 'vue-router'
import LandingPage from '../views/LandingPage.vue'

Vue.use(VueRouter)

const router = new VueRouter({
  mode: 'history',
  base: import.meta.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'LandingPage',
      component: LandingPage
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../components/RegisterForm.vue')
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../components/LoginForm.vue')
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../components/AdminDashboard.vue')
    },
    {
      path: '/moviedetails',
      name: 'moviedetails',
      component: () => import('../components/MovieDetails.vue')
    },
    {
      path: '/movielist',
      name: 'movielist',
      component: () => import('../components/MovieList.vue')
    },
    {
      path: '/moviemanagement',
      name: 'moviemanagement',
      component: () => import('../components/MovieManagement.vue')
    },
    {
      path: '/showtimemanagement',
      name: 'showtimemanagement',
      component: () => import('../components/ShowtimeManagement.vue')
    },
    {
      path: '/theatredetails',
      name: 'theatredetails',
      component: () => import('../components/TheatreDetails.vue')
    },
    {
      path: '/theatremanagement',
      name: 'theatremanagement',
      component: () => import('../components/TheatreManagement.vue')
    },
    {
      path: '/theatreadd',
      name: 'theatreadd',
      component: () => import('../components/TheatreAdd.vue')
    },
    {
      path: '/showedit',
      name: 'showedit',
      component: () => import('../components/ShowEdit.vue')
    },
    {
      path: '/theatreedit/:theatreCode',
      name: 'theatreedit',
      component: () => import('../components/TheatreEdit.vue')
    },

    {
      path: '/userdashboard',
      name: 'userdashboard',
      component: () => import('../components/UserDashboard.vue')
    }
  ]
})

export default router
