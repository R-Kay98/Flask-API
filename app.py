import json
import requests
import requests_cache
from flask import Flask, request, Response
requests_cache.install_cache('api_cache')
app = Flask(__name__)

class Post:
    def __init__(self, post):
        self.author = post['author']
        self.authorId = post['authorId']
        self.id = post['id']
        self.likes = post['likes']
        self.popularity = post['popularity']
        self.reads = post['reads']
        self.tags = post['tags']

class Posts:
    def __init__(self, tags, sortBy, direction):
        self.tags = tags
        self.sortBy = sortBy
        self.direction = direction
        self.posts = []
        self.postsExist = {}
        self.baseURL = 'https://api.hatchways.io/assessment/blog/posts?tag='
    
    def postExists(self, postID):
        '''
        This function will write the JSON output containing the student's course and test grades.
        The output is exactly that of the sample file.
        
        INPUTS
            postID : int, mandatory
                Unique identifier of each post. This is used to efficiently ensure that no duplicate posts
                are added to the list of posts.                
        
        RETURNS
            True/False : boolean
                True signifies that the post-to-be is a duplicate of an already existing one, and therefore
                should not be added to the list of posts.
        '''
        
        if postID in self.postsExist:
            return True
        self.postsExist[postID] = True
        return False

    def sortPosts(self):
        '''
        This function will sort the posts list, which contains instances of each Post, according to the
        sortBy and direction parameters.        
        
        INPUTS
            None.
        
        RETURNS
            None.
        '''
        
        if self.direction == 'desc':
            rev = True
        else:
            rev = False
        if self.sortBy == 'reads':
            self.posts.sort(key=lambda x: x.reads, reverse=rev)
        elif self.sortBy == 'likes':
            self.posts.sort(key=lambda x: x.likes, reverse=rev)
        elif self.sortBy == 'popularity':
            self.posts.sort(key=lambda x: x.popularity, reverse=rev)
        else:
            self.posts.sort(key=lambda x: x.id, reverse=rev)
    
    def setPosts(self):
        '''
        This function will make a number pof individual requests to the baseURL, consistent with the number
        of tags provided in the API call. For each individual call, the dictionary values will be parsed and
        stored into a list of Post instances, after which it's sorted according to the sortBy and direction
        parameters.        
        
        INPUTS
            None.
        
        RETURNS
            None.
        '''
        
        for tag in self.tags:
            r = requests.get(self.baseURL+tag)
            allPosts = json.loads(r.text)['posts']
            for postContent in allPosts:
                if not self.postExists(postContent['id']):
                    post = Post(postContent)
                    self.posts.append(post)
        self.sortPosts()
    
    def getPosts(self):
        '''
        This function will write the JSON output containing the student's course and test grades.
        The output is exactly that of the sample file.
        
        INPUTS
            None.
        
        RETURNS
            responseJSON : str, initially a dict but converted to JSON
                Contains the sorted and accumulated final API response in JSON format.
        '''
        
        responseJSON = {'posts': []}
        for post in self.posts:
            intermJSON = {
                'author': post.author,
                'authorId': post.authorId,
                'id': post.id,
                'likes': post.likes,
                'popularity': post.popularity,
                'reads': post.reads,
                'tags': post.tags
            }
            responseJSON['posts'].append(intermJSON)
        return json.dumps(responseJSON)

def checkValidInput(tags, sortBy, direction):
    '''
    This function will write the JSON output containing the student's course and test grades.
    The output is exactly that of the sample file.
    
    INPUTS
        tags : list, mandatory
            List of all the tags in the API call.
        sortBy : str, mandatory
            Field by which the posts will be sorted.
        direction : str, mandatory
            Determines whether the sorting is ascending or descending.
    
    RETURNS
        Message : str
            If the input is not valid, a JSON string containing the error message is returned.
    '''
    
    possibleSortByValues = ['id', 'reads', 'likes', 'popularity']
    possibleDirectionValues = ['asc', 'desc']
    
    if tags[0] == '':
        return json.dumps({'error': 'Tags parameter is required'})
    elif sortBy not in possibleSortByValues:
        return json.dumps({'error': 'sortBy parameter is required'})
    elif direction not in possibleDirectionValues:
        return json.dumps({'error': 'Direction parameter is required'})
    return None

def tagsInTagList(tags, tagList):
    '''
    Helper function that determines whether at least one tag in the tags parameter is present
    in the tagList.
    
    INPUTS
        tags : list, mandatory
            List of tags in the API call.
        tagList : list, mandatory
            List of tags in a particular post.
    
    RETURNS
        True/False : boolean
            If at least one tag in the API call is present in the post tags, True is returned.
    '''
    
    for tag in tags:
        if tag in tagList:
            return True
    return False

def verifyTags(req, tags):
    '''
    This function will write the JSON output containing the student's course and test grades.
    The output is exactly that of the sample file.
    
    INPUTS
        req : str, mandatory
            Url link of the API call to be made.
        tags : list, mandatory
            List of tags present in the API call query parameters.
    
    RETURNS
        Message : str
            Passed if the test is successful, Failed otherwise.
    '''
    
    r = requests.get(req)
    posts = json.loads(r.text)['posts']

    for post in posts:
        if len(tags) > 1:
            print(tags)
            print(post['tags'])
        if tagsInTagList(tags, post['tags']) == False:
            return 'Failed'
    return 'Passed'

def verifyOrderDesc(req, key):
    '''
    This function verifies that the API response entries have a consistent descending order.
    
    INPUTS
        req : str, mandatory
            Url link of the API call to be made.
        key : str, mandatory
            Key corresponding to the Post value by which we want to verify the ordering.
    
    RETURNS
        Message : str
            Passed if the test is successful, Failed otherwise.
    '''
    
    tempValue = 999999
    r = requests.get(req)
    posts = json.loads(r.text)['posts']
    
    for post in posts:
        if tempValue < post[key]:
            return 'Failed'
        tempValue = post[key]
    return 'Passed'

def verifyOrderAsc(req, key):
    '''
    This function verifies that the API response entries have a consistent ascending order.
    
    INPUTS
        req : str, mandatory
            Url link of the API call to be made.
        key : str, mandatory
            Key corresponding to the Post value by which we want to verify the ordering.
    
    RETURNS
        Message : str
            Passed if the test is successful, Failed otherwise.
    '''
    
    tempValue = -999999
    r = requests.get(req)
    posts = json.loads(r.text)['posts']
    
    for post in posts:
        if tempValue > post[key]:
            return 'Failed'
        tempValue = post[key]
    return 'Passed'

def pingTest(req):
    '''
    This function verifies that the ping API response yields the expected output.
    
    INPUTS
        req : str, mandatory
            Url link of the API call to be made.
    
    RETURNS
        Message : str
            Passed if the test is successful, Failed otherwise.
    '''
    
    r = requests.get(req)
    expectedResult = '{"success": true}'
    
    if r.text == expectedResult:
        return 'Passed'
    return 'Failed'

def invalidParameter(req):
    '''
    This function verifies that an invalid API response request yields the expected error message(s).
    
    INPUTS
        req : str, mandatory
            Url link of the API call to be made.
    
    RETURNS
        Message : str
            Passed if the test is successful, Failed otherwise.
    '''
    
    r = requests.get(req)
    
    if 'error' in r.text:
        return 'Passed'
    return 'Failed'

def testRoutes():
    '''
        This function contains will perform all the appropriate API calls to thoroughly test the functionality
        and response of each call. The invalid parameters, API ping, final order and tags present will all be
        checked.
        
        INPUTS
            None.
        
        RETURNS
            testCases : str, initially a dict but converted to JSON.
                Contains a list of each test case and whether each individual case passed or failed.
    '''
    
    testCases = {}
    reqOne = 'http://127.0.0.1:5000/api/posts?tags=&sortBy=popularity&direction=desc'
    reqTwo = 'http://127.0.0.1:5000/api/posts?tags=tech&sortBy=nothing&direction=desc'
    reqThree = 'http://127.0.0.1:5000/api/posts?tags=tech&sortBy=popularity&direction=none'
    reqFour = 'http://127.0.0.1:5000/api/ping'
    reqFive = 'http://127.0.0.1:5000/api/posts?tags=tech&sortBy=popularity&direction=asc'
    reqSix = 'http://127.0.0.1:5000/api/posts?tags=tech&sortBy=popularity&direction=desc'
    reqSeven = 'http://127.0.0.1:5000/api/posts?tags=tech&sortBy=id&direction=desc'
    reqEight = 'http://127.0.0.1:5000/api/posts?tags=tech&sortBy=reads&direction=desc'
    reqNine = 'http://127.0.0.1:5000/api/posts?tags=tech&sortBy=likes&direction=desc'
    reqTen = 'http://127.0.0.1:5000/api/posts?tags=history&sortBy=likes&direction=desc'
    reqEleven = 'http://127.0.0.1:5000/api/posts?tags=tech,history&sortBy=likes&direction=desc'
    testCases['No tags'] = invalidParameter(reqOne)
    testCases['Invalid sortBy'] = invalidParameter(reqOne)
    testCases['Invalid direction'] = invalidParameter(reqOne)
    testCases['Api ping'] = pingTest(reqFour)
    testCases['Ascending order popularity'] = verifyOrderAsc(reqFive, 'popularity')
    testCases['Descending order popularity'] = verifyOrderDesc(reqSix, 'popularity')
    testCases['Descending order id'] = verifyOrderDesc(reqSeven, 'id')
    testCases['Descending order reads'] = verifyOrderDesc(reqEight, 'reads')
    testCases['Descending order likes'] = verifyOrderDesc(reqNine, 'likes')
    testCases['Tags tech'] = verifyTags(reqNine, ['tech'])
    testCases['Tags history'] = verifyTags(reqTen, ['history'])
    testCases['Tags tech & history'] = verifyTags(reqEleven, ['tech', 'history'])
    return json.dumps(testCases)

@app.route("/")
def base():
    return "Initial page"
    
@app.route("/api/tests")
def test():
    testCases = testRoutes()
    return testCases, 200
    
@app.route("/api/ping")
def ping():
    myJsonResponse = {'success': True}
    myJsonResponse = json.dumps(myJsonResponse)
    return myJsonResponse, 200
    
@app.route("/api/posts")
def posts():
    tags = request.args.get('tags', default = '', type=str).split(',')
    sortBy = request.args.get('sortBy', default='id', type=str)
    direction = request.args.get('direction', default='asc', type=str)
    errorResponse = checkValidInput(tags, sortBy, direction)
    
    if errorResponse != None:
        return errorResponse, 400
    
    allPosts = Posts(tags, sortBy, direction)
    allPosts.setPosts()
    responseJSON = allPosts.getPosts()
    return responseJSON, 200
    
if __name__ == "__main__":
    app.run(debug=True)