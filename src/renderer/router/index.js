import Vue from 'vue'
import Router from 'vue-router'

// import Home from '../components/Home'
import BlankSlate from '../components/BlankSlate'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      // component: Home
      component: BlankSlate
    },
    {
      path: '/count_downs',
      name: 'count_downs',
      // component: require('@/components/CountDowns').default
      component: BlankSlate
    },
    {
      path: '/log_entries',
      name: 'log_entries',
      // component: require('@/components/LogEntries').default
      component: BlankSlate
    },
    {
      path: '/notes',
      name: 'notes',
      // component: require('@/components/Notes').default
      component: BlankSlate
    },
    {
      path: '/scratch_pad',
      name: 'scratch_pad',
      // component: require('@/components/ScratchPad').default
      component: BlankSlate
    },
    {
      path: '/secrets',
      name: 'secrets',
      // component: require('@/components/Secrets').default
      component: BlankSlate
    },
    {
      path: '/timeoff',
      name: 'timeoff',
      // component: require('@/components/TimeOff').default
      component: BlankSlate
    },
    {
      path: '/todos',
      name: 'todos',
      // component: require('@/components/Todos').default
      component: BlankSlate
    },
    {
      path: '/work_days',
      name: 'work_days',
      // component: require('@/components/WorkDays').default
      component: BlankSlate
    },
    {
      path: '*',
      redirect: '/'
    }
  ]
})
