import Vue from 'vue'
import Router from 'vue-router'

// import BlankSlate from '../components/BlankSlate'
import Home from '../components/Home'
import CountDowns from '../components/CountDowns'
import LogEntries from '../components/LogEntries'
import Notes from '../components/Notes'
import ScratchPad from '../components/ScratchPad'
import Secrets from '../components/Secrets'
import TimeOff from '../components/TimeOff'
import Todos from '../components/Todos'
import WorkDays from '../components/WorkDays'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/count_downs',
      name: 'count_downs',
      component: CountDowns
    },
    {
      path: '/log_entries',
      name: 'log_entries',
      component: LogEntries
    },
    {
      path: '/notes',
      name: 'notes',
      component: Notes
    },
    {
      path: '/scratch_pad',
      name: 'scratch_pad',
      component: ScratchPad
    },
    {
      path: '/secrets',
      name: 'secrets',
      component: Secrets
    },
    {
      path: '/timeoff',
      name: 'timeoff',
      component: TimeOff
    },
    {
      path: '/todos',
      name: 'todos',
      component: Todos
    },
    {
      path: '/work_days',
      name: 'work_days',
      component: WorkDays
    },
    {
      path: '*',
      redirect: '/'
    }
  ]
})
