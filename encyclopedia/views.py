import markdown2
from django import forms
from django.shortcuts import render

from . import util

class NewSearchForm(forms.Form):
    search = forms.CharField(label="Search")

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

def search(request):
    if request.method == 'POST':
        query = request.POST.get('value', '')
        print(query)
        search_value = util.get_entry(query)
        if search_value:
            search_value = markdown2.markdown(search_value)
        else: 
            return render(request, "encyclopedia/list.html", {
            "entries": util.list_entries()
            })

        return render(request, "encyclopedia/search.html", {
            "search": search_value
    })