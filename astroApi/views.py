from django.http import JsonResponse
import json
from skyfield.api import load, Topos, Star
from skyfield.data import hipparcos
from datetime import datetime
from datetime import timezone

navigationStarsHip = {
    'Acamar':	13847,
    'Achernar':	7588,
    'Acrux':	60718,
    'Adhara':	33579,
    'Aldebaran':	21421,
    'Alioth':	62956,
    'Alkaid':	67301,
    'Alnair':	109268,
    'Alnilam':	26311,
    'Alphard':	46390,
    'Alphecca':	76267,
    'Alpheratz':	677,
    'Altair':	97649,
    'Ankaa':	2081,
    'Antares':	80763,
    'Arcturus':	69673,
    'Atria':	82273,
    'Avior':	71129,
    'Bellatrix':	25336,
    'Betelgeuse':	27989,
    'Canopus':	30438,
    'Capella':	24608,
    'Deneb':	102098,
    'Denebola':	57632,
    'Diphda':	3419,
    'Dubhe':	54061,
    'Elnath':	25428,
    'Eltanin':	87833,
    'Enif':	107315,
    'Fomalhaut':	113368,
    'Gacrux':	61084,
    'Gienah':	59803,
    'Hadar':	68702,
    'Hamal':	9884,
    'Kaus Australis':	90185,
    'Kochab':	72607,
    'Markab':	113963,
    'Menkar':	14135,
    'Menkent':	68933,
    'Miaplacidus':	45238,
    'Mirfak':	15863,
    'Nunki':	92855,
    'Peacock':	100751,
    'Pollux':	37826,
    'Procyon':	37279,
    'Rasalhague':	86032,
    'Regulus':	49669,
    'Rigel':	24436,
    'Rigil Kent':	71683,
    'Sabik':	84012,
    'Shedir':	3179,
    'Shaula':	85927,
    'Sirius':	32349,
    'Spica':	65474,
    'Suhail':	44816,
    'Vega':	91262,
    'Zuben’ubi':	72622,
}



def index(request):
    stars = []

    if request.body:
        req = json.loads(request.body)

        if req['type'] == 'GET_VISIBLE_STARS':
            planets = load('de421.bsp')
            earth = planets['earth']
            ts = load.timescale()
            dt = datetime.strptime(req['date'], '%Y-%m-%dT%H:%M:%S.%fZ')
            dt = dt.replace(tzinfo=timezone.utc)
            t = ts.utc(dt)
            observerLocation = earth + \
                Topos(latitude_degrees=req['lat'],
                        longitude_degrees=req['long'])

            with load.open(hipparcos.URL) as f:
                df = hipparcos.load_dataframe(f)
            
            for key in navigationStarsHip:
                starname = key
                hipNo = navigationStarsHip[key]
                star = Star.from_dataframe(df.loc[hipNo])

                apparent = observerLocation.at(t).observe(star).apparent()
                alt, az, dist = apparent.altaz()
                eachStar = {
                    'name': key,
                    'hip': navigationStarsHip[key],
                    'alt': alt.degrees,
                    'az': az.degrees,
                    'dist': dist.km
                }
                if eachStar['alt'] > 0 :
                    stars.append(eachStar)


        if req['type'] == 'GET_TBRG_STAR':
            planets = load('de421.bsp')
            earth = planets['earth']
            ts = load.timescale()
            dt = datetime.strptime(req['date'], '%Y-%m-%dT%H:%M:%S.%fZ')
            dt = dt.replace(tzinfo=timezone.utc)
            t = ts.utc(dt)
            observerLocation = earth + \
                Topos(latitude_degrees=req['lat'],
                        longitude_degrees=req['long'])

            with load.open(hipparcos.URL) as f:
                df = hipparcos.load_dataframe(f)

                starname = req['selectedStar']
                hipNo = navigationStarsHip[starname]
                star = Star.from_dataframe(df.loc[hipNo])
                apparent = observerLocation.at(t).observe(star).apparent()
                alt, az, dist = apparent.altaz()

                return JsonResponse({
                    'name': starname,
                    'hipNo': navigationStarsHip[starname],
                    'alt': alt.degrees,
                    'az': az.degrees,
                    'dist': dist.km
                })


        if (req['type'] == 'GET_TBRG_PLANET'):
            planets = load('de421.bsp')
            earth = planets['earth']
            ts = load.timescale()
            dt = datetime.strptime(req['date'], '%Y-%m-%dT%H:%M:%S.%fZ')
            dt = dt.replace(tzinfo=timezone.utc)
            t = ts.utc(dt)
            observerLocation = earth + \
                Topos(latitude_degrees=req['lat'],
                        longitude_degrees=req['long'])

            planet = planets[req['body']]
            apparent = observerLocation.at(t).observe(planet).apparent()
            alt, az, dist = apparent.altaz()
            return JsonResponse({
                "alt": alt.degrees,
                "az": az.degrees,
                "dist": dist.km
            })
