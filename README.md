# interviewSeason: Tesla

To use tesla_challenge_allison.py:
1. Clone repo to get python file.
2. Then run "python tesla_challenge_allison.py"
3. This will initiate the http server at: http://127.0.0.1:5000/
4. From here you can add queries with the following functions:
	- AddNode(name)
	- AddRoute(firstNode, secondNode, distance)
	- GetFastestRoute(firstNode, secondNode)
5. In order to create the queries, here are some examples of what to type in the server bar:
	- For adding nodes: http://127.0.0.1:5000/AddNode/A/
	- For creating routes: http://127.0.0.1:5000/AddRoute/A/B/3/ (This will print an error if either of the nodes don't exist)
	- For finding the fastest route: http://127.0.0.1:5000/GetFastestRoute/A/B/ (This will print an error if the path is not possible)
