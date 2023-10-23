import markdown2

from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def content(request, entry):

    entry = util.get_entry(entry)
    if entry:
        entry = markdown2.markdown(entry)
    else: 
        return render(request, "encyclopedia/notfound.html", {
            "error": entry
        })

    return render(request, "encyclopedia/content.html", {
        "entry": entry
    })

# def direct_view(request):

#     entry = request.GET.get('entry')
#     return render(request, "encyclopedia/content.html", {
#         "entry": entry
#     })