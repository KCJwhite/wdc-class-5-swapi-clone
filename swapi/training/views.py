import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


def text_response(request):
    """
    Return a HttpResponse with a simple text message.
    Check that the default content type of the response must be "text/html".
    """
    return HttpResponse("Hey you got it")


def looks_like_json_response(request):
    """
    Return a HttpResponse with a text message containing something that looks
    like a JSON document, but it's just "text/html".
    """
    return HttpResponse("Looks like - {'some': 'data'}")


def simple_json_response(request):
    """
    Return an actual JSON response by setting the `content_type` of the HttpResponse
    object manually.
    """
    return HttpResponse(json.dumps({'some' :'data'}), content_type="application/json")


def json_response(request):
    """
    Return the same JSON document, but now using a JsonResponse instead.
    """
    return JsonResponse({'some': 'data'})


def json_list_response(request):
    """
    Return a JsonReponse that contains a list of JSON documents
    instead of a single one.
    Note that you will need to pass an extra `safe=False` parameter to
    the JsonResponse object it order to avoid built-in validation.
    https://docs.djangoproject.com/en/2.0/ref/request-response/#jsonresponse-objects
    """
    return JsonResponse([{'a': 1}, {'b': 2}, {'c': 3}], safe=False)


def json_error_response(request):
    """
    Return a JsonResponse with an error message and 400 (Bad Request) status code.
    """
    return JsonResponse('Un problemo', status=400, safe=False)


@csrf_exempt
def only_post_request(request):
    """
    Perform a request method check. If it's a POST request, return a message saying
    everything is OK, and the status code `200`. If it's a different request
    method, return a `400` response with an error message.
    """
    if request.method == 'POST':
        return JsonResponse({'good': 'job'}, status=200)
    else:
        return JsonResponse({'screwed': 'up'}, status=400)


@csrf_exempt
def post_payload(request):
    """
    Write a view that only accepts POST requests, and processes the JSON
    payload available in `request.body` attribute.
    """
    if request.method == 'POST':
        try:
            stuff = json.loads(request.body)
        except:
            HttpResponse("Not valid JSON.")
        return HttpResponse(f"Thanks for {stuff}")
    else:
        return HttpResponse("Bad method")


def custom_headers(request):
    """
    Return a JsonResponse and add a custom header to it.
    """
    response = JsonResponse({'some': 'thing'})
    response['Custom Header'] = "Yeah"
    return response


def url_int_argument(request, first_arg):
    """
    Write a view that receives one integer parameter in the URL, and displays it
    in the response text.
    """
    return HttpResponse(f"Your value is {str(first_arg)}")


def url_str_argument(request, first_arg):
    """
    Write a view that receives one string parameter in the URL, and displays it
    in the response text.
    """
    return HttpResponse(f"Your value is {first_arg}")


def url_multi_arguments(request, first_arg, second_arg):
    """
    Write a view that receives two parameters in the URL, and display them
    in the response text.
    """
    return HttpResponse(f"Your values are {first_arg} and {second_arg}")


def get_params(request):
    """
    Write a view that receives GET arguments and display them in the
    response text.
    """
    return HttpResponse(f"{request.META['QUERY_STRING']}")
