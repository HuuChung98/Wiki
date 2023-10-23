import markdown2

from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def content(request, name):

    entry = util.get_entry(name)
    if entry:
        entry = markdown2.markdown(entry)
    else: 
        return render(request, "encyclopedia/notfound.html", {
            "error": name
        })

    return render(request, "encyclopedia/content.html", {
        "entry": entry
    })