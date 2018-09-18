## HW 1
## SI 364 F18
## 1000 points

#################################

## List below here, in a comment/comments, the people you worked with on this assignment AND any resources you used to find code (50 point deduction for not doing so). If none, write "None".

#none

## [PROBLEM 1] - 150 points
## Below is code for one of the simplest possible Flask applications. Edit the code so that once you run this application locally and go to the URL 'http://localhost:5000/class', you see a page that says "Welcome to SI 364!"

from flask import Flask, render_template, request
import requests
import json


app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_to_you():
    return 'Hello!'

@app.route('/class')
def hello_class():
    return 'Welcome to SI364!'


## [PROBLEM 2] - 250 points
## Edit the code chunk above again so that if you go to the URL 'http://localhost:5000/movie/<name-of-movie-here-one-word>' you see a big dictionary of data on the page. For example, if you go to the URL 'http://localhost:5000/movie/ratatouille', you should see something like the data shown in the included file sample_ratatouille_data.txt, which contains data about the animated movie Ratatouille. However, if you go to the url http://localhost:5000/movie/titanic, you should get different data, and if you go to the url 'http://localhost:5000/movie/dsagdsgskfsl' for example, you should see data on the page that looks like this:

# {
#  "resultCount":0,
#  "results": []
# }


## You should use the iTunes Search API to get that data.
## Docs for that API are here: https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
## Of course, you'll also need the requests library and knowledge of how to make a request to a REST API for data.

## Run the app locally (repeatedly) and try these URLs out!

@app.route('/movie/<moviename>')
def movie_info(moviename):
	base_url = 'https://itunes.apple.com/search'
	params_diction = {'term':str(moviename), 'entity':'movie'}
	params_diction['term'] = moviename
	response = requests.get(base_url, params = params_diction)
	text = response.text
	obj = json.loads(text)
	return str(obj)

## [PROBLEM 3] - 250 points

## Edit the above Flask application code so that if you run the application locally and got to the URL http://localhost:5000/question, you see a form that asks you to enter your favorite number.
## Once you enter a number and submit it to the form, you should then see a web page that says "Double your favorite number is <number>". For example, if you enter 2 into the form, you should then see a page that says "Double your favorite number is 4". Careful about types in your Python code!
## You can assume a user will always enter a number only.

@app.route('/question')
def fav_number():
	htmlform = '''
	<html>
	<body>
	<h1>Enter your Favorite Number</h1>
	<form method = 'GET' action = 'http://localhost:5000/result'>
		Favorite Number:<br>
		<input type = 'Number' name= 'Number'>
		<input type = 'Submit' value = 'Submit'>
	</form>
	</body>
	</html>'''
	return htmlform

@app.route('/result', methods = ['GET'])
def doubled():
	if request.method == 'GET':
		num = request.args.get('Number')
		doubled = str(int(num)*2)
	return 'Doube your favorite number is {}'.format(doubled)



## [PROBLEM 4] - 350 points

## Come up with your own interactive data exchange that you want to see happen dynamically in the Flask application, and build it into the above code for a Flask application, following a few requirements.

## You should create a form that appears at the route: http://localhost:5000/problem4form

## Submitting the form should result in your seeing the results of the form on the same page.

## What you do for this problem should:
# - not be an exact repeat of something you did in class
# - must include an HTML form with checkboxes and text entry
# - should, on submission of data to the HTML form, show new data that depends upon the data entered into the submission form and is readable by humans (more readable than e.g. the data you got in Problem 2 of this HW). The new data should be gathered via API request or BeautifulSoup.

# You should feel free to be creative and do something fun for you --
# And use this opportunity to make sure you understand these steps: if you think going slowly and carefully writing out steps for a simpler data transaction, like Problem 1, will help build your understanding, you should definitely try that!

# You can assume that a user will give you the type of input/response you expect in your form; you do not need to handle errors or user confusion. (e.g. if your form asks for a name, you can assume a user will type a reasonable name; if your form asks for a number, you can assume a user will type a reasonable number; if your form asks the user to select a checkbox, you can assume they will do that.)

# Points will be assigned for each specification in the problem.

@app.route('/problem4form', methods = ["GET", "POST"])
def itunessearch():
	form = '''
	<html>
	<body>
	<h1>What do you want to search iTunes for? </h1>
	<form method = 'GET' action = 'http://localhost:5000/problem4form'>
		Search:
		<input type = 'text' name= 'term'> <br>
		<input type = 'checkbox' name = 'media' value = 'movie'> Movie<br>
		<input type = 'checkbox' name = 'media' value = 'podcast'> Podcast<br>
		<input type = 'checkbox' name = 'media' value = 'music'> Music<br>
		<input type = 'checkbox' name = 'media' value = 'audiobook'> Audiobook<br>
		<input type = 'submit' value = 'Submit'> <br>
	</form>
	</body>
	</html>
	'''


	if request.method == "GET":
		mediatype = request.values.get('media')
		termtype= request.values.get('term')
		url= 'https://itunes.apple.com/search'
		params_diction = {}
		# params_diction['media'] = mediatype
		# params_diction['term'] = termtype
		params_diction = {'media':mediatype, 'term': termtype}
		response = requests.get(url, params = params_diction)
		text = response.text
		obj = json.loads(text)
		# print (obj)
		info = ''
		result= '<h1> Results for search:\n</h1>'
		for item in obj['results']:
			kind = item['kind']
			name = item['trackName']
			statement = '\n{}, {}\n <br>'.format(name, kind)
			info += statement
		return form + result + info



if __name__ == '__main__':
    app.run()
