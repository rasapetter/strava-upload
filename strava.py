import json, os
import argparse
import requests

UPLOAD_URL = "https://www.strava.com/api/v3/uploads"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload activities to Strava.')
    parser.add_argument("access_token", metavar="ACCESS_TOKEN")
    parser.add_argument("filepath", metavar="FILE")
    parser.add_argument('--activity', dest='activity_type', default='run', help='Activity type. Possible values: possible values: ride, run, swim, workout, hike, walk, nordicski, alpineski, backcountryski, iceskate, inlineskate, kitesurf, rollerski, windsurf, workout, snowboard, snowshoe. Default: run.')
    parser.add_argument('--type', dest='data_type', default=None, help='Data type. Strava supports FIT, TCX and GPX. Default: use file extension.')
    parser.add_argument('--name', dest='name', default=None, help='Activity name. Defaults to a combination of position and date.')
    parser.add_argument('--desc', dest='description', default=None, help='Activity description.')
    args = parser.parse_args()

    filepath = args.filepath
    if not os.path.isfile(filepath):
        print "Can't open %s" % filepath
        exit()

    data_type = args.data_type
    if not data_type and "." in filepath:
        data_type = os.path.splitext(filepath)[1][1:]
    if not data_type:
        print "Missing data type"
        exit()
    data_types = ['fit', 'tcx', 'gpx']
    if data_type.lower() not in data_types:
        print "Unsupported data type. Expected one of: %s" % ", ".join(data_types)
        exit()

    params = {
        'activity_type': args.activity_type,
        'data_type': data_type.lower()
        #'private'
    }
    if args.name: params['name'] = args.name
    if args.description: params['description'] = args.description

    # Upload the file.
    r = requests.post(UPLOAD_URL, params=params, files={
        'file': open(filepath, 'rb')
    }, headers={
        'Authorization': 'Bearer %s' % args.access_token
    })

    # Handle the response.
    response = r.text
    try:
        response = json.loads(response)
    except: pass

    if r.status_code not in [200,201]:
        if 'error' in response and response['error']:
            print "Error: %s" % response['error']
        else:
            print "Error: Failed to upload %s" % filepath
        exit()

    if 'status' in response:
        print "Strava: %s" % response['status']
        exit()

    print "Activity uploaded."
