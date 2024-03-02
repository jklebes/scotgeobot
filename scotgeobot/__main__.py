from scotgeobot.calcGeohashes import *
from scotgeobot.checkCities import *
from scotgeobot.checkStations import *
from scotgeobot.scotgeobot import *
from scotgeobot.homealerts import *
from plyer import notification
from os import path
import argparse

project_directory = path.dirname(path.abspath(__file__))

if __name__=="__main__":
    # TODO make arg parsing a function in scotgeobot?
    # argparser
    parser = argparse.ArgumentParser()
    # whether to broadcast
    parser.add_argument('--toot', action=argparse.BooleanOptionalAction, default=False)
    # skip desktop alerts in favor of command line
    parser.add_argument('--desktop', action=argparse.BooleanOptionalAction, default=True)
    # force re-check of old dates
    parser.add_argument('-f', '--redo', action='store_true')
    # include homealert in main module run?
    parser.add_argument('--homealert', action='store_true')

    # a debugging run would be '--redo -no--desktop' and a production run would be '--toot' only
    args = parser.parse_args()
    tooting = args.toot;
    desktop = args.desktop;
    redo = args.redo;
    homealert = args.homealert;

    mastodon_account=None
    if tooting:
        try:
            from mastodon import Mastodon
        except:
            print("Optional dependency mastodon not installed, cannot proceed as mastodon bot.")
            print("Try ")
            print("       pip install mastodon")
            tooting=False 
        import requests
    if tooting:
        # maybe find instance url saved from last run 
        server_found = False
        # try looking in saved mastodon_host.txt for instance from last time
        mastodon_host_file =path.join(project_directory,"data", "mastodon_host.txt")
        if path.isfile(mastodon_host_file):
            # read path
            f = open(mastodon_host_file, 'r')
            api_base_url = f.readline()
            f.close()
            # try reaching it
            response = requests.get(api_base_url)
            if response.status_code == 200:
                server_found = True
            else:
                print("The instance ", api_base_url , " was used last time, but now it can't be reached.")

        # maybe find token.secret from saved path last run
        token_found = False
        token_path_file =path.join(project_directory,"data", "token_path.txt")
        if path.isfile(token_path_file):
            # read path
            f = open(token_path_file, 'r')
            token_path = f.readline()
            f.close()
            # check if this is a valid path 
            if path.isfile(token_path):
                token_found = True
        
        # user message
        if not server_found or not token_found:
            print("You are setting up scotgeobot to post to a mastodon account.")
            print("You should set up a mastodon account and save the Personal Access Token in a file.")
        
        # interactive setup or instance url and api token path
        attempts=0
        while not server_found and attempts<3:
            print("Enter your instance [Default botsin.space, press ENTER to proceed with default]:")
            url_entered=input().strip()
            if len(url_entered)==0:
                api_base_url='https://botsin.space/'
            else:
                # add https://, / if nor present
                if url_entered[0:8]!="https://":
                    #strip initial : , / , .
                    api_base_url = url_entered.strip(":/\,")
                    api_base_url = "https:// "+ api_base_url + "/"
                    # add "https://"
                else:
                    api_base_url = url_entered.rstrip("\/")
                    api_base_url = api_base_url + "/"
                # try reaching this url
            response = requests.get(api_base_url)
            if response.status_code == 200:
                server_found = True
                # remember instance
                f = open(mastodon_host_file, 'w')
                f.write(api_base_url)
                f.close()
            else:
                print("Could not reach " , api_base_url, " .")
                attempts +=1 #try a few more times
        attempts=0
        if server_found:
            while not token_found and attempts<3:
                # setting up Personal Access Token:
                # try looking in default location ~/.mastodon/token.secret
                print("Please enter the file path of your Personal Access Token [default ~/.mastodon/token.secret, press ENTER to use default]")
                entered_path = input().strip()
                if len(entered_path) == 0:
                    token_path = path.join(path.expanduser('~'), ".mastodon", "token.secret")
                    print("Looking for Personal Access Token file in default location ", token_path," .")
                else:
                    # check, format path string?
                    token_path = entered_path
                    print("Looking for Personal Access Token file in ", token_path)
                if path.isfile(token_path):
                    token_found=True
                    # print success
                    print("Setting up mastodon account")
                    # remember location
                    f = open(token_path_file, 'w')
                    f.write(token_path)
                    f.close()
                else:
                    # try a few more times
                    attempts+=1
        if server_found and token_found:
            try:
                mastodon_account = Mastodon(
                    access_token= token_path,
                    api_base_url= api_base_url)
            except:
                print("Failed to connect to mastodon account at ", api_base_url, " with Personal Access Token at ", token_path, ".")
                tooting = False
        else:
            tooting = False

    # despite user flag --toot, tooting was set back to False because of failure to import mastodon,
            # set up url or access token, or set up Mastodon() object
    if args.toot and not tooting:
        if desktop:
            output_type = "desktop notification"
        else:
            output_type = "command line interface"
        print("Failed to connect to a mastodon account, proceeding with ", output_type, " output.")


    last_dates= getLastDates(datefile=datefile, dateformat=dateformat)
    dates_digits = geohash_digits()
    nd = newDates([date for (date, offset) in dates_digits], last_dates)
    if redo:
        nd = [date for date,offset in dates_digits];
    results = geohashes(scotland_graticules, [(date, offset)
                     for (date, offset) in dates_digits if date in nd])
    hits=0
    for date in results:
        coords=results[date]
        # scotland-specific sign, subtract from negative longitudes
        cities = checkCities(coords)
        for c in cities:
            text = "Geohash in " + c + " on " + date.strftime(dateformat) + "."
            notify(text,desktop, tooting, mastodon_account)
            hits += 1
        stations = checkStations(coords)  # dict listos of (s,c) by graticule
        for g in stations:
            stations_graticule = stations[g]
            text = "Geohash near "
            for s, c in stations_graticule[:-1]:
                if s.split()[-1] == "Station":
                    text = text + s + \
                        " (" + str(round(c[0], 3)) + ", " + str(round(c[1], 3)) + "), "
                else:
                    text = text + s + \
                        " station (" + str(round(c[0], 3)) + ", " + str(round(c[1], 3)) + "), "
            (s, c) = stations_graticule[-1]
            if len(stations_graticule) > 1:
                text = text + "and "
            if s.split()[-1] == "Station":
                text = text + s + \
                    " (" + str(round(c[0], 3)) + ", " + str(round(c[1], 3)) + ") "
            else:
                text = text + s + \
                    " station (" + str(round(c[0], 3)) + ", " + str(round(c[1], 3)) + ") "
            text = text + "on " + date.strftime(dateformat) + "."
            notify(text, desktop, tooting, mastodon_account)
            hits += 1
        if homealert:
            for coord in results[date]:
                dist = dist_km(home, coord)
                # print(dist, date)
                if dist <= homedist:
                    text = "Geohash " + str(round(dist)) + \
                        "km from me on " + str(date) + "!"
                    # mastodon.status_post(text)
                    notify(text, desktop, tooting=False)

    # write dates to file
    f = open(path.join(project_directory, "data", datefile), 'w')
    for (date, offset) in dates_digits:
        f.write(date.strftime(dateformat) + '\n')
    f.close()
