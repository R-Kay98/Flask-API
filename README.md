# Flask-API
Simple API that fetches data from the API: <https://api.hatchways.io/assessment/blog/posts>. Includes the following:
* Tags: Some number of tags with comma-separated strings starting with the 'tags' parameter. E.g: tags=tech,history.
* Sort By: One of 'id', 'reads', 'likes' or 'popularity' starting with the 'sortBy' parameter. E.g: sortBy=id.
* Direction: One of 'asc' or 'desc' starting with the 'direction' parameter. E.g: direction=asc. 

## Getting Started
* Install dependencies 
`pip install -r requirements.txt`

* Run the flask script in the Flask directory
`python app.py`

* Once flask is running, to get the posts simply go to a webbrowser and type:
<http://127.0.0.1:5000/api/posts?tags=<tags>&sortBy=<sortBy>&direction=<direction>>

* The sortBy and direction parameters are both optional but will send an error if 
incorrectly entered.

* To test the API connectivity, go to:
<http://127.0.0.1:5000/api/ping>

* To run some tests, go to:
<http://127.0.0.1:5000/api/tests>
