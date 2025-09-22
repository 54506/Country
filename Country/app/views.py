from django.shortcuts import render
import requests

def index(request):
    form = True
    l = []

    if request.method == "POST":
        country = request.POST.get('country')
        form = False
        data = requests.get(f"paste your api here {country}").json()

        for i in data:
            d = {}
            # Names
            d['name_common'] = i['name']['common']
            d['name_official'] = i['name']['official']

            # Independence
            d['independent'] = i.get('independent', 'Not available')

            # Currency
            if 'currencies' in i:
                curr = list(i['currencies'].values())[0]
                d['currency_name'] = curr.get('name', 'Not available')
                d['currency_symbol'] = curr.get('symbol', '')
            else:
                d['currency_name'] = 'Not available'
                d['currency_symbol'] = ''

            # Country codes
            d['cca2'] = i.get('cca2', '')
            d['cca3'] = i.get('cca3', '')
            d['ccn3'] = i.get('ccn3', '')

            # INR specifically
            d['inr'] = 'Yes' if 'INR' in i.get('currencies', {}) else 'No'

            # Calling code
            if 'idd' in i and 'root' in i['idd'] and 'suffixes' in i['idd']:
                d['calling_code'] = i['idd']['root'] + ''.join(i['idd']['suffixes'])
            else:
                d['calling_code'] = 'Not available'

            # Capital
            d['capital'] = ', '.join(i.get('capital', ['Not available']))

            # Region & Subregion
            d['region'] = i.get('region', 'Not available')
            d['subregion'] = i.get('subregion', 'Not available')

            # Languages
            d['languages'] = list(i.get('languages', {}).values())

            # Latitude & Longitude
            latlng = i.get('latlng', [None, None])
            d['latitude'] = latlng[0] if len(latlng) > 0 else 'Not available'
            d['longitude'] = latlng[1] if len(latlng) > 1 else 'Not available'

            # Borders shared
            d['borders'] = i.get('borders', [])

            # Area & Population
            d['area'] = i.get('area', 'Not available')
            d['population'] = i.get('population', 'Not available')

            # Timezones
            d['timezones'] = i.get('timezones', [])

            # Maps
            d['googleMaps'] = i.get('maps', {}).get('googleMaps', '#')
            d['openStreetMaps'] = i.get('maps', {}).get('openStreetMaps', '#')

            # Coat of Arms
            coat = i.get('coatOfArms', {}).get('png')
            d['coatOfArms'] = coat if coat else "Not available"

            # Flag
            flag = i.get('flags', {}).get('png')
            d['flags'] = flag if flag else "Not available"

            l.append(d)

    context = {'form': form, 'l': l}
    return render(request, 'index.html', context)


