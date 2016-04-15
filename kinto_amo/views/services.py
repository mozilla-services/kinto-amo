from cliquet import Service


path = '/blocklist/{api_ver}/{application_guid}/{application_ver}/'

blocklist = Service(name="blocklist", path=path,
                    description="Blocklist data")


@blocklist.get()
def get_blocklist(request):
    api_ver = request.matchdict['api_ver']
    app = request.matchdict['application_guid']
    app_ver = request.matchdict['application_ver']
    query = request.body

    return {
        'API version': api_ver,
        'Application': app,
        'Application version': app_ver,
        'Query': query}
