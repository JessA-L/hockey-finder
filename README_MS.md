# Hockey Soonest/Cheapest Microservice

### To request data from this microservice
<pre>
1. Run it in the same directory as tm-results.json.

2. Have applicable event information stored in tm-results.json 
   from ticketmaster-api.

3. Create/write to microservice_command.txt with the text "run".

with open('microservice_command.txt', 'w') as outfile:
    outfile.write('run')

3. The microservice will then find the soonest and cheapest tickets
   from tm-results.json and output to the microservice_results.json.

4. It will also update microservice_command.txt to a blank txt file.
</pre>
### To receive data from this microservice
<pre>
5. Once microservice_command.txt is a blank txt file then you know the 
   microservice_results.json has been updated.

6. The microservice outputs a list with two nested lists. index [0] is 
   a list of the soonest games while index [1] is a list of the cheapest 
   games. If there are more than one that is the cheapest or the soonest
   then multiple will be in the nested lists. If there is no price data
   then cheapest will be an empty list.

7. Load the json file.

example:
with open('microservice_results.json', 'r') as microservice_results:
    soonest_cheapest = json.load(microservice_results)

8. Access nested lists.

example prints each event name in soonest/cheapest indices:
soonest = soonest_cheapest[0]
cheapest = soonest_cheapest[1]

for event in soonest:
    print(soonest[event]['name'])

for event in cheapest:
    print(cheapest[event]['name'])
</pre>