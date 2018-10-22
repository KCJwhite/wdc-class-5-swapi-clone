import json
import pdb
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView
from django.utils.decorators import method_decorator
from django.core import serializers

from api.models import Planet, People
from api.fixtures import SINGLE_PEOPLE_OBJECT, PEOPLE_OBJECTS
from api.serializers import serialize_people_as_json


def single_people(request):
    return JsonResponse(SINGLE_PEOPLE_OBJECT)


def list_people(request):
    return JsonResponse(PEOPLE_OBJECTS, safe=False)


@csrf_exempt
def people_list_view(request):
    """
    People `list` actions:

    Based on the request method, perform the following actions:

        * GET: Return the list of all `People` objects in the database.

        * POST: Create a new `People` object using the submitted JSON payload.

    Make sure you add at least these validations:

        * If the view receives another HTTP method out of the ones listed
          above, return a `400` response.

        * If submited payload is nos JSON valid, return a `400` response.
    """
    pass

class PeopleListView(ListView):
    model = People

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        LIST_ALLOWED_METHODS = ['GET', 'POST']
        if request.method.upper() in LIST_ALLOWED_METHODS:
            return super(PeopleListView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponse('Not an allowed HTTP method', status=400)

    def get(self, *args, **kwargs):
        all_people = list(People.objects.values())
        return JsonResponse(all_people, safe=False)

    def post(self, *args, **kwargs):
        try:
            data = json.loads(self.request.body.decode('UTF-8'))
            People.objects.create(**data)
            print("After")
            return JsonResponse({'POST': 'Success', 'data': data})
        except ValueError:
            return JsonResponse({'POST': 'Failed', 'Problem': 'Data not valid JSON'}, status=400)


@csrf_exempt
def people_detail_view(request, people_id):
    """
    People `detail` actions:

    Based on the request method, perform the following actions:

        * GET: Returns the `People` object with given `people_id`.

        * PUT/PATCH: Updates the `People` object either partially (PATCH)
          or completely (PUT) using the submitted JSON payload.

        * DELETE: Deletes `People` object with given `people_id`.

    Make sure you add at least these validations:

        * If the view receives another HTTP method out of the ones listed
          above, return a `400` response.

        * If submited payload is nos JSON valid, return a `400` response.
    """
    pass



class PeopleDetailView(DetailView):
    model = People

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        DETAIL_ALLOWED_METHODS = ['GET', 'PUT', 'PATCH', 'DELETE']
        if request.method.upper() in DETAIL_ALLOWED_METHODS:
            return super(PeopleDetailView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponse(f"Allowed methods when specifying an id are: {DETAIL_ALLOWED_METHODS}", status=400)

    
    def _get_object(self, people_id):
        try:
            return People.objects.get(pk=people_id)
        except People.DoesNotExist:
            return None

    
    def get(self, request, *args, **kwargs):
        people_id = kwargs.get('people_id')
        if people_id:
            people = self._get_object(people_id)
            if not people:
                return JsonResponse({"GET": "Failed", "Problem": "Person not found."}, status=404)
            data = serialize_people_as_json(people)
        return JsonResponse(data, status=200, safe=False)

    
    def delete(self, *args, **kwargs):
        people_id = kwargs.get('people_id')
        if not people_id:
            return JsonResponse({"DELETE": "Failed", "Problem": "No person specified."}, status=400)
        people = self._get_object(people_id)
        if not people:
            return JsonResponse({"DELETE": "Failed", "Problem": f"Couldn't find anyone with id: {people_id}"}, status=400)
        people.delete()
        return JsonResponse({"DELETE": "Success"}, status=200, safe=False)

    def _update(self, people, payload, partial=False):
        for field in ['name', 'homeworld', 'height', 'mass', 'hair_color']:
            if not field in payload:
                if partial:
                    continue
                return JsonResponse({"Update": "Failed", "Problem": "Missing field for full update."}, status=400)
            try:
                if field is 'homeworld':
                    payload[field] = Planet.objects.get(pk=payload[field])
                setattr(people, field, payload[field])
                people.save()
            except ValueError:
                return JsonResponse({"Update": "Failed", "Problem": "Provided payload isn't valid."}, status=400)
        data = serialize_people_as_json(people)
        return JsonResponse(data, status=200, safe=False)

    def patch(self, *args, **kwargs):
        people_id = kwargs.get('people_id')
        people = self._get_object(people_id)
        if not people:
            return JsonResponse({"PATCH": "Failed", "Problem": f"Couldn't find anyone with id: {people_id}"}, status=404)

        try:
            payload = json.loads(self.request.body)
        except ValueError:
            return JsonResponse({"PATCH": "Failed", "Problem": "Not valid JSON."}, status=400)
        return self._update(people, payload, partial=True)

    def put(self, *args, **kwargs):
        people_id = kwargs.get('people_id')
        people = self._get_object(people_id)
        if not people:
            return JsonResponse({"PUT": "Failed", "Problem": f"Couldn't find anyone with id: {people_id}"}, status=404)
        try:
            payload = json.loads(self.request.body)
        except ValueError:
            return JsonResponse({"PUT": "Failed", "Problem": "Not valid JSON."}, status=400)
        return self._update(people, payload, partial=False)
