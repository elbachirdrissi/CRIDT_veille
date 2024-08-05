import requests
from django.shortcuts import render
from duckduckgo_search import DDGS

def form(request):
    if request.method == 'GET':
        search_engine_id = '431a89fa13ec54cb9'
        api_key = 'AIzaSyCtMXRhH3nGQICfhVc7Zs4zIKlaQWcv8hE'
        
        search_query = request.GET.get('search_query', '')
        if not search_query :
            return render(request, 'pages/form.html', {'error': 'La requête de recherche est nécessaire.'})

        searchType = request.GET.get('searchType', '')
        fileType = request.GET.get('fileType', '')
        lr = request.GET.get('lr', '')
        cr = request.GET.get('cr', '')
        sort = 'date' if request.GET.get('sort') else ''
        start = request.GET.get('start', '')
        num = request.GET.get('num', '')
        
        numD = request.GET.get('numD', 10)
        try:
            numD = int(numD)
        except ValueError:
            numD = 10
        
        exactTerms = request.GET.get('exactTerms', '')
        excludeTerms = request.GET.get('excludeTerms', '')
        
        siteSearch = request.GET.get('siteSearch', '')
        sites = [site.strip() for site in siteSearch.split(',')] if siteSearch else ['']
        checked_sites = request.GET.getlist('proposition')
        sites.extend(checked_sites)
        siteSearchFilter = 'i' if request.GET.get('siteSearchFilter') else 'e'
        
        dateDebut = request.GET.get('dateDebut', '')
        dateFin = request.GET.get('dateFin', '')
        dateRestrict = f"{dateDebut}:{dateFin}" if dateDebut and dateFin else ''
        imgSize = request.GET.get('imgSize', '')
        imgColorType = request.GET.get('imgColorType', '')
        
        
        #Google custom search result
        url = 'https://www.googleapis.com/customsearch/v1'
        google_result = []
        for site in sites:
            parameters = {
                'key': api_key,
                'cx': search_engine_id,
                'q': search_query,
                'searchType': searchType,
                'fileType': fileType,
                'lr': lr,
                'cr': cr,
                'sort': sort,
                'start': start,
                'num': num,
                'exactTerms': exactTerms,
                'excludeTerms': excludeTerms,
                'siteSearch': site,
                'siteSearchFilter': siteSearchFilter,
                'dateRestrict': dateRestrict, 
                'imgSize': imgSize,
                'imgColorType': imgColorType,
                
            }
            parameters = {k: v for k, v in parameters.items() if v}
        
            response = requests.get(url, params=parameters)
            Gresults = response.json().get('items', [])
            google_result.extend(Gresults)
            
            
        #DuckDuckGo result
        duckduckgo_results = []
        Dresults = DDGS().text(
            keywords = search_query,
            region = 'wt-wt',
            safesearch = 'off',
            timelimit='7d',
            max_results = numD
        )
        for Dresult in Dresults:
            duckduckgo_results.append({
                'title': Dresult.get('title', ''),
                'link': Dresult.get('href', '')
            })


        return render(request, 'pages/form.html', {
            'Gresults': google_result,
            'Dresults': duckduckgo_results,
            'checked_sites': checked_sites
            })
    
    return render(request, 'pages/form.html')