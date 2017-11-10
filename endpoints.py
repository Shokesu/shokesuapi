
'''
Este script define los endpoints de la API de shokesu (métodos y rutas)
e.g:
str(update_user) == 'POST /register'
update_user.method == 'POST'
update_user.path == '/register'

Los endpoints pueden tener placeholders...
add_terms_to_proyect.path == 'POST /site/$1/terms'
add_terms_to_proyect.placeholders == ['site']

Para rellenar los placeholders...

add_terms_to_proyect.path(site = 'mysite') == '/site/mysite/terms'

También se añade documentación sobre la API de shokesu.
'''


class PathWrapper:
    def __init__(self, path, placeholders=[]):
        self.path = path
        self.placeholders = placeholders

    def __call__(self, **kwargs):
        path = self.path
        for i in range(0, len(self.placeholders)):
            placeholder = self.placeholders[i]
            try:
                path = path.replace('${}'.format(i+1), kwargs[placeholder])
            except:
                raise ValueError('No value for "{}" placeholder on "{}" endpoint'.format(placeholder, str(self)))
        return path

    def __str__(self):
        return self.path

class Endpoint:
    def __init__(self, method, path, placeholders = []):
        self.method = method
        self.path = PathWrapper(path, placeholders)
        self.placeholders = placeholders

    def __str__(self):
        return '{} {}'.format(self.method, self.path)



register_user = Endpoint(
    method = 'POST',
    path = '/register',
    placeholders = []
)

update_user = Endpoint(
    method = 'PUT',
    path = '/user/$1',
    placeholders = ['user']
)

delete_user = Endpoint(
    method = 'DELETE',
    path = '/user/$1',
    placeholders = ['user']
)

"""
@api {get} /site/:site_id/terms Add terms to a proyect
@apiName AddTermsToProyect
@apiDescription Add some terms to a existing proyect
@apiGroup Proyects
@apiParam {String} site_id Unique ID that identifies the proyect
@apiHeader {String} Authorization This should be "Bearer JWT", where JWT is a js web token. 
@apiHeaderExample {json} Header-Example:
    {
        "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ"
    }
"""
add_terms_to_proyect = Endpoint(
    method = 'POST',
    path = '/site/$1/terms',
    placeholders = ['site']
)


add_profile_to_proyect = Endpoint(
    method = 'POST',
    path = '/site/$1/getprofiles',
    placeholders = ['site']
)


"""
@api {get} /site/:site_id Get proyect info
@apiName GetProyectInfo
@apiDescription Retrieve avaliable proyect information
@apiGroup Proyects
@apiParam {String} site_id Unique ID that identifies the proyect
@apiHeader {String} Authorization This should be "Bearer JWT", where JWT is a js web token. 
"""
get_proyect_info = Endpoint(
    method = 'GET',
    path = '/site/$1',
    placeholders = ['site']
)


"""
@api {get} /profile/:profile_id Get Profile info
@apiName GetProfileInfo
@apiDescription Get information of a monitorized profile
@apiGroup Profiles
@apiParam {String} profile_id Unique ID that identifies the profile
@apiHeader {String} Authorization This should be "Bearer JWT", where JWT is a js web token. 
"""
get_profile_info = Endpoint(
    method = 'GET',
    path = '/profile/$1',
    placeholders = ['profile']
)

"""
@api {post} /site/<profile_id>/posts Get profile posts

@apiName GetProfilePosts
@apiDescription Get posts published by a monitorized profile.
The fields of the response explained below, defines the data returned per post.
The response in fact, is a JSON Object list, which is able to contain multiple elements inside
of it (one entry per post)
The payload of the request must be encoded as a valid JSON object.
@apiGroup Profiles
@apiHeader {String} Authorization This should be "Bearer JWT", where JWT is a js web token.

@apiParam {String} profile_id It should be replaced <b>in the URL</b> with the unique ID of the profile
@apiParam {Integer} page_number This parameter can be used to paginate the results and indicate
the page number to retrieve the posts from (<b>This parameter should be added to the URL</b>)
@apiParam {Integer} page_size Indicates the page size. The response of this request will
contain at most as many post as this parameter quantity (<b>This parameter should be added to the URL</b>)
@apiParam {String} sort Can be used to sort the posts.
Possible values are: <b>published_at, retweets_asc, retweets_desc, likes_asc, likes_desc</b>
(<b>This parameter should be added to the URL</b>)
@apiParam {Object} filter This can be used to filter the posts to be retrieved. 
You can indicate multiple filters in this JSON object, see the "<a href="filters">filters</a>" section
(<b>This parameter should be included in the payload of the request</b>)

@apiSuccess {String} mongoid Unique ID identifier of this post in Shokesu mongo DB database
@apiSuccess {Integer} post_id The ID of the post
@apiSuccess {String[]} videos
@apiSuccess {String} source The user's device system that published this post (e.g: android)
@apiSuccess {Object} body Contains the message of the post. Is a JSON object with only one entry.
That entry contains a key whose value is the language of the post (e.g: "en", "es") and the body of the
post as its value.
@apiSuccess {String[]} pictures
@apiSuccess {String} url The external url reference to the post.
@apiSuccess {String[]} concepts
@apiSuccess {String} provider Indicates the social network source of this post (e.g: "twitter", "facebook"...)
@apiSuccess {String[]} entities
@apiSuccess {String[]} original_tags
@apiSuccess {String} lang Indicates the language of the post
@apiSuccess {String} kind
@apiSuccess {Integer} channel_id Indicates the profile ID (in mongoDB) of the user that sent this post.
<b>This field is only avaliable when the profile is added to some proyect (not only monitorized)</b>

@apiSuccess {Integer} favorite_count Amount of users that marked the post as favorite
@apiSuccess {Integer} reach_count Amount of users that had been reached by the post
@apiSuccess {Date} published_at Indicates when the post was published at.
It follows the next format: <b>yyyy-mm-ddThh:mm+0000</b>

@apiSuccess {Boolean} is_retweet Indicates whatever this post is a retweet or not. <b>This field is only avaliable for twitter posts.</b>
@apiSuccess {Integer} retweet_count Number of times that this post had been retweeted.<b>This field is only avaliable for twitter posts.</b>
@apiSuccess {Boolean} is_reply Indicates if this post is a reply to another post.<b>This field is only avaliable for twitter posts.</b>

@apiSuccessExample {json} Success-Response
HTTP/1.1 200 OK
    [
        {
            "post_id" : "...",
            "provider" : "...",
            "body" : {
                "es" : "@FooBar Hello World!"
            },
            "url" : "https://www.twitter.com/status/...",
            "published_at" : "2017-08-31T11:19+0000",
            ...
        },
        {
            ...
        }
    ]
"""
get_profile_posts = Endpoint(
    method = 'POST',
    path = '/profile/$1/posts',
    placeholders = ['profile']
)

"""
@api {post} /profile/<profile_id>/site/<site_id>/posts Get profile posts on proyect
@apiName GetProfilePostsOnProyect
@apiDescription Get posts published by a monitorized profile in a proyect.
To check all the parameters and fields in the response, check this <a href="#api-Profiles-GetProfilePosts">request</a>, which is
practically the same thing; The only difference is that this request add the parameter 
"site_id" to the URL.
@apiGroup Profiles
@apiHeader {String} Authorization This should be "Bearer JWT", where JWT is a js web token. 
@apiParam {String} profile_id Unique ID that identifies the profile
@apiParam {String} site_id Unique ID that identifies the proyect (It should be passed <b>in the URL</b>)
@apiParam {String} profile_id It should be replaced <b>in the URL</b> with the unique ID of the profile

"""
get_profile_posts_on_proyect = Endpoint(
    method = 'POST',
    path = '/profile/$1/site/$2/posts',
    placeholders = ['profile', 'site']
)



"""
@api {get} /site/:site_id/getprofiles Get profiles
@apiName GetProfiles
@apiDescription Get profiles list added to a proyect
@apiGroup Profiles
@apiParam {Number} site_id Unique ID that identifies the proyect
@apiHeader {String} Authorization This should be "Bearer JWT", where JWT is a js web token. 
"""
get_profiles = Endpoint(
    method = 'POST',
    path = '/site/$1/getprofiles',
    placeholders = ['site']
)

get_graphs = Endpoint(
    method = 'POST',
    path = '/site/$1/dashboard/$2',
    placeholders = ['site', 'dashboard']
)

get_reports = Endpoint(
    method = 'GET',
    path = '/site/$1/report/$2',
    placeholders = ['site', 'report']
)

get_insights = Endpoint(
    method = 'POST',
    path = '/profile/$1/pdfReport',
    placeholders = ['profile']
)