Suggestion for tickets with long duration and group switches

* Ignore tickets with more than N group switches
* Average per group: Duration = (Total duration) / (number of group switches)
* For newer tickets, check out the field "u_ticket_lifecycle" which holds the
  history for the group switches that has occurred


Response time:

* Run query and cache the results
* Need persistant storage
* No need to re-run the same tickets since the response time won't change

1. Get list of all incidents/requests
2. For each ticket:
  1. Get the history and sort by date ASC (e.g. https://cerntraining.service-now.com/api/now/table/sys_history_line?sysparm_query=set.id=<ticket sys_id>)
  2. For each entry, query the user and see which department they belong to
  3. When a user belongs to the selected department, do a time diff of when the ticket was assigned to the group and the opening date time

* Cache each ticket that has been calculated
* Calculate all the new tickets each time the script is executed
* Average response time = (response time of all cached tickets + response time of all new tickets) / (cached ticket count + new ticket count)