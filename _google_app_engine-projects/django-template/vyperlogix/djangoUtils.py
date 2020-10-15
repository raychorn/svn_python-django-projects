def parse_url_parms(request):
    import urllib
    return [urllib.unquote_plus(t.strip()) for t in request.META['PATH_INFO'].split('/') if (len(t.strip()) > 0)]

