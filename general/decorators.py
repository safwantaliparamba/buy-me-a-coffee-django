import json

from django.http.response import HttpResponse

from rest_framework.response import Response


def group_required(group_names):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs) :
            if request.user.is_authenticated:
                if not bool(request.user.groups.filter(name__in=group_names)) | request.user.is_superuser:
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        response_data = {}
                        response_data['status'] = 'false'
                        response_data['stable'] = 'true'
                        response_data['title'] = 'Permission Denied'
                        response_data['message'] = "You have no permission to do this action."
                        # return HttpResponse(json.dumps(response_data), content_type='application/javascript')
                        return Response(response_data)
                    else:
                        context = {
                            "title" : "Permission Denied"
                        }
                        return HttpResponse('<h1>Permission Denied</h1>')

            return view_method(request, *args, **kwargs)

        return _arguments_wrapper

    return _method_wrapper
