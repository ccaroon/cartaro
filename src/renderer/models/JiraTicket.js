import Resource from './Resource'

// -----------------------------------------------------------------------------
class JiraTicket extends Resource {
  static RESOURCE_NAME = 'jira'

  color () {
    var color = 'blue'

    if (this.status === 'In Progress') {
      color = 'green'
    } else if (this.status === 'Closed') {
      color = 'red'
    }

    return color
  }
}
// -----------------------------------------------------------------------------
export default JiraTicket
