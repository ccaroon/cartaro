import Icon from '../lib/Icon'
import Resource from './Resource'
// -----------------------------------------------------------------------------
class JiraTicket extends Resource {
  static RESOURCE_NAME = 'jira'

  icon () {
    return Icon.search(this.type, 'mdi-ticket-confirmation')
  }

  color () {
    let color = 'blue'

    if (this.status === 'In Progress') {
      color = 'green'
    } else if (this.status === 'Closed') {
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
