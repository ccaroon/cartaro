import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: require('@/components/Home').default
    },
    {
      path: '/log_entries',
      name: 'log_entries',
      component: require('@/components/LogEntries').default
    },
    {
      path: '/notes',
      name: 'notes',
      component: require('@/components/Notes').default
    },
    {
      path: '*',
      redirect: '/'
    }
  ]
})
