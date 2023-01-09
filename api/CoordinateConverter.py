import requests
import xml.etree.ElementTree as ET

# Convert WGS84 coordinates to Lmb72 using an external API: http://zoologie.umons.ac.be/tc/
def DegToLmb72(lat, long):
    url = "http://zoologie.umons.ac.be/tc/ws/Coordinates.asmx?"
    headers = {'content-type' : 'application/soap+xml'}
    body = """<?xml version="1.0" encoding="utf-8"?>
    <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
    <soap12:Body>
        <DegToLmb72 xmlns="http://zoologie.umh.ac.be/">
        <Latitude>""" +str(lat)+ """</Latitude>
        <Longitude>"""+str(long)+"""</Longitude>
        <Datum>WGS84</Datum>
        </DegToLmb72>
    </soap12:Body>
    </soap12:Envelope>"""

    response  = requests.post(url, data=body, headers=headers) # send a POST request to the API to get converted coordinates
    #print (response.text)
    #the response looks like this:
    #<?xml version="1.0" encoding="utf-8"?>
    #   <soap:Envelope
    #        xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
    #        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    #        xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    #        <soap:Body>
    #            <DegToLmb72Response
    #                xmlns="http://zoologie.umh.ac.be/">
    #                <DegToLmb72Result>
    #                    <x>VALUE</x>
    #                    <y>VALUE</y>
    #                </DegToLmb72Result>
    #            </DegToLmb72Response>
    #        </soap:Body>
    #    </soap:Envelope>

    xmlResponse = ET.fromstring(response.content) # convert the string to an XML Tree
    DegToLmb72Result = xmlResponse[0][0][0] #navigate to the DegToLmb72Result
    x = float(DegToLmb72Result[0].text)
    y = float(DegToLmb72Result[1].text)
    return [x,y] #return the x & y coordinates in Lmb72

#
def Lmb2008ToLmb72(x,y,z):
    return [x,y,z]

#CoordinateSystem { Lambert72, Lambert2008, WGS84 }
def ConvertFromJson(coordinateDict, type):
    if(type == 0):
        return [coordinateDict["x"],coordinateDict["y"],coordinateDict["z"]]
    elif(type == 1):
        return Lmb2008ToLmb72(coordinateDict["x"],coordinateDict["y"],coordinateDict["z"])
    elif(type == 2):
        lmbCoords = DegToLmb72(coordinateDict["y"],coordinateDict["x"])
        return(lmbCoords[0], lmbCoords[1],coordinateDict["z"])

def helloworld():
    print("Hello world")