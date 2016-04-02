from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Category, Page
from django.contrib.auth import authenticate, login, logout
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.bing_search import run_query
from django.shortcuts import redirect
from django import template

def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5] #upto 5 step 2 query the model
    page_list = Page.objects.order_by('-views')[:5]
    context_dict= {'boldmessage': "hi there", 'categories': category_list,'pages': page_list } #step 3 pass results to
    #new added#  # green letter is the context the reference to data
    #page_list = Page.objects.order_by('-views')[:5]
    #context_dict= {'page': page_list}
    #With the query complete, we passed a reference to the list (stored as variable category_list)
    # to the dictionary, context_dict. This dictionary is then passed as part of the context for
    # the template engine in the render() call.

    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, we default to zero and cast that. 1 is yes

    #visits = int(request.COOKIES.get('visits','1'))
    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
    #response = render(request, 'rango/index.html',context_dict)

    #### return HttpResponse("Rango says hey there world! <br/> <a href='/rango/about'> About </a>")
    # Does the cookie last_visit exist?last visit is given variable
    #if 'last_visit' in request.COOKIES:
        # Yes it does! Get the cookie's value.
     #   last_visit = request.COOKIES['last_visit']
        # Cast the value to a Python date/time object.
      #  last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        # If it's been more than a day since the last visit...
        if (datetime.now() - last_visit_time).seconds > 5:
            visits = visits + 1
 # ...and flag that the cookie last visit needs to be updated
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
 # Cookie last_visit doesn't exist, so flag that it should be set.
        reset_last_visit_time = True

       # context_dict['visits'] = visits
#Obtain our Response object early so we can add cookie information.
       # response = render(request, 'rango/index.html', context_dict)

    if reset_last_visit_time:
        #server get cookie from request data
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits
        #client side get cookie from response send by serer
        #response.set_cookie('last_visit', datetime.now()) un client site
        #response.set_cookie('visits', visits)
    #return this back to client
    response = render(request, 'rango/index.html', context_dict)
    return response

#added
#def page(request):
 #   page_list = Page.objects.order_by('-views')[:5]
  #  context_dict= {'pages': page_list}

    #With the query complete, we passed a reference to the list (stored as variable category_list)
    # to the dictionary, context_dict. This dictionary is then passed as part of the context for
    # the template engine in the render() call.

    # Render the response and send it back!  template context
   # return render(request, 'rango/index.html',context_dict)
def about(request):
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0
    context_dict= {'linemessage': "a simple line message" } #add as template
    context_dict['visits'] = count
    return render(request, 'rango/about.html', context_dict)

#detailed categry pages
def category(request, category_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}
    context_dict['result_list'] = None
    context_dict['query'] = None
    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

            context_dict['result_list'] = result_list
            context_dict['query'] = query

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category'] = category
        context_dict['category_name'] = category.name
        context_dict['category_name_slug'] = category.slug
        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category).order_by('-views')
        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.


    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us
        #from index template
        pass
        # Go render the response and return it to the client.
    if not context_dict['query']:
        context_dict['query'] = category.name

    return render(request, 'rango/category.html', context_dict)


@login_required
def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database
            form.save(commit=True)
            # print cat, cat.slug
            # Now call the index() view.
            # The user will be shown the homepage.
            # back to the home page
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST its GET, display the form to enter details.
        #this will appear to user first then post request
        form = CategoryForm()
        # Bad form (or form details), no form supplied...
        # Render the form with error messages (if any) to user
    return render(request, 'rango/add_category.html',{'form':form})

#add page form to a given category
@login_required
def add_page(request,category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if cat:
                page = form.save(commit = False)
                page.category = cat
                page.views = 0
                page.save()
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()
    context_dict = {'form':form, 'category': cat}
#render to post request
    return render (request, 'rango/add_page.html', context_dict)

#in views is the logic pass whatever i like//url mapping pass request!

def register(request):
    #if request.session.test_cookie_worked():
     #   print "test cookie worked"
      #  request.session.delete_test_cookie()
        # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST) #object
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            #create user instance user object
            user = user_form.save()
            #hash password, once hashed update the user object
            user.set_password(user.password)
            user.save()
            #Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            # Now we save the UserProfile model instance.
            profile.save()
            # Update our variable to tell the template registration was successful.
            registered = True
        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user
        else:
            print user_form.errors, profile_form.errors
 # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'rango/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form. provided by django
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.

        if user:
            if user.is_active:
               # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)  # no need to create log in form use django provied on e
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("your rango account is disabled") # no need template to del with this
        else:
            print "invalid login details: {0}, {1}".format(username, password)

            return HttpResponse("invalid login details supplied")
 # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        return render(request, 'rango/login.html', {})

#no template no form only view and url and index.html
@login_required
def restricted(request):
    return HttpResponse("you are logged in so you can see this text")

@login_required
def user_logout(request):

    logout(request)

    return HttpResponseRedirect('/rango/')


def search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            result_list = run_query(query)

    return render(request, 'rango/search.html', {'result_list': result_list})

#def track_url(request):
 #   page_id = None
  #  url = '/rango/'
   # if request.method == 'GET':
    #    if 'page_id' in request.GET:
     #       page_id = request.GET['page_id']
      #      try:
       #         page = Page.Objects.get(id=page_id)
        #        page.views = page.views + 1
         #       page.save()
          #      url = page.url
           # except:
            #    pass

   # return redirect(url)


def track_url(request):
    page_id = None
    url = '/rango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass

    return redirect(url)


@login_required
def like_category(request):

    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes =  likes
            cat.save()

    return HttpResponse(likes)

#helper function we use a filter to find all the categories that start with the string supplied

register = template.Library()

@register.inclusion_tag('rango/cats.html')

def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__istartswith=starts_with)

    if max_results > 0:
        if cat_list.count() > max_results:
            cat_list = cat_list[:max_results]

    return cat_list

def suggest_category(request):
    cat_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']

    cat_list = get_category_list(8, starts_with)
    return render(request, 'rango/cats.html', {'cat_list': cat_list })





































