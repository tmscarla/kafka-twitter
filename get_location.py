import geocoder
import reverse_geocoder as rg
import pprint

def reverseGeocode():
    g = geocoder.ip('me')
    print(g.latlng)
    # Coorinates tuple.Can contain more than one pair.
    coordinates =(g.latlng[0], g.latlng[1])
    result = rg.search(coordinates)
    # result is a list containing ordered dictionary.
    #print(f"{result[0]['name']}, {result[0]['cc']}")
    print(result)

# Driver function
if __name__=="__main__":
    reverseGeocode()
