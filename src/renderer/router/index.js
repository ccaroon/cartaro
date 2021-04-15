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
      path: '/count_downs',
      name: 'count_downs',
      component: require('@/components/CountDowns').default
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
      path: '/scratch_pad',
      name: 'scratch_pad',
      component: require('@/components/ScratchPad').default
    },
    {
      path: '/secrets',
      name: 'secrets',
      component: require('@/components/Secrets').default
    },
    {
      path: '/todos',
      name: 'todos',
      component: require('@/components/Todos').default
    },
    {
      path: '/work_days',
      name: 'work_days',
      component: require('@/components/WorkDays').default
    },
    {
      path: '*',
      redirect: '/'
    }
  ]
})
