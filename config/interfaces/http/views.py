from django.shortcuts import render

PAGES = {
    "module-1": "Information provision",
    "module-2": "Publication production",
    "module-4": "Infrastructure & operations",
    "sources": "Data sources",
    "import": "Import & data quality",
    "reports": "Reports",
}


def dashboard(request):
    return render(request, "dashboard.html", {"nav_active": "overview", "page_title": "Overview"})


def placeholder(request, key):
    return render(request, "placeholder.html", {"nav_active": key, "page_title": PAGES[key]})
