import Icon from '../lib/Icon'
import Resource from './Resource'
// -----------------------------------------------------------------------------
class JiraTicket extends Resource {
  static RESOURCE_NAME = 'jira'

  icon () {
    let icon = null
    if (this.status === 'Blocked') {
      icon = Icon.get('cancel')
    } else {
      icon = Icon.search(this.type, 'mdi-ticket-confirmation')
    }

    return icon
  }

  color () {
    let color = 'blue'

    if (this.status === 'In Progress') {
      color = 'green'
    } else if (this.status === 'Closed') {
      color = 'red'
    } else if (this.status === 'Blocked') {
      color = 'red'
    }

    return color
  }

  toString () {
    return this.summary
  }
}
// -----------------------------------------------------------------------------
export default JiraTicket
