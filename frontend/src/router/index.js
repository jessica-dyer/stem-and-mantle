// Composables
import { createRouter, createWebHistory } from 'vue-router'
import HardcodedForm from "../components/HardcodedForm.vue";


const routes = [
  {
    path: '/',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "home" */ '@/views/Home.vue'),
      },
      {
        path: 'hardcoded-form', // This is the URL path for the HardcodedForm component
        name: 'HardcodedForm', // Optional name for the route
        component: HardcodedForm, // The HardcodedForm component you want to display
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
