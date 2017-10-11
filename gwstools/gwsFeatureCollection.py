import requests
import pygplates

#proxies = {'http':''}


def FeatureCollection(model='MULLER2016',layer='rotations',url='http://gws.gplates.org',proxy=''):
# function to access gpml data files directly from the gplates-web-service data store 
# and load them into pygplates feature collections.
# options for the 'layer' are:
# - 'rotations'
# - 'coastlines'
# - 'static_polygons'
# - 'plate_polygons'
#

    if layer=='rotations':
        requested_file = 'request.rot'
    else:
        requested_file = 'request.gpmlz'

        with open(requested_file, 'wb') as handle:
            r = requests.get('%s/model/get_model_layer/?model=%s&layer=%s' % (url,model,layer),
                             proxies={'http':'%s' % proxy},
                             stream=True)

            if r.status_code!=200:
                error_string = 'Remote request returned with message %s' % r.text
                raise Exception(error_string)
            else:
               for block in r.iter_content(1024):
                   handle.write(block)

            if layer=='rotations':
                result = pygplates.RotationModel('request.rot')
            else:
                result = pygplates.FeatureCollection('request.gpmlz')

    return result

