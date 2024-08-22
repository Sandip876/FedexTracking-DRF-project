# from rest_framework.views import APIView
# from rest_framework.response import Response
# from decouple import config
# import requests
# import json



# def auth_fedex():
#     try:
#         data = {
#             'grant_type': 'client_credentials',
#             'client_id':config('FEDEX_API_KEY'),
#             'client_secret': config('FEDEX_SECRET_KEY')
#         }
        
#         # headers
#         headers = {
#             'Content-Type': "application/x-www-form-urlencoded"
#         }
        
#         # Make a api call 
#         response = requests.post(f"{config("FEDEX_BASE_API_URL")}/oauth/token", data=data, headers=headers)
#         return response.json()
#     except Exception as e:
#         print("Error authenticating with fedex API",e)
#         return ValueError("Failed to  authenticate with fedex API")

# class FedexTrackingView(APIView):
#     def get(self, req):
#         auth_res = auth_fedex()
#         # Input data
#         data = json.dumps({
#             'includeDetailedScans':True,
#             'trackinginfo': [
#                 {
#                     'trackingNumberInfo': {
#                         'trackingNumber': 122816215025810
#                     }
#                 }
#             ]
#         })
#         headers = {
#             'Content-Type': "application/json",
#             'X-locale': "en_US",
#             'Authorization': "Bearer "+auth_res["access_token"]
#         }
#         # Make a api call 
#         response = requests.post(f"{config("FEDEX_BASE_API_URL")}/track/v1/trackingnumbers", data=data, headers=headers)
#         print(response)
#         if response.status_code == 200:
#             return Response({"Tracking Details": response.text})
#         else:
#             return Response({"Error":'Failed to fetch the  tracking information'}, status=response.status_code)


from rest_framework.views import APIView
from rest_framework.response import Response
from decouple import config
import requests
import json

def auth_fedex():
    try:
        data = {
            'grant_type': 'client_credentials',
            'client_id': config('FEDEX_API_KEY'),
            'client_secret': config('FEDEX_SECRET_KEY')
        }
        
        # headers
        headers = {
            'Content-Type': "application/x-www-form-urlencoded"
        }
        
        # Make a api call 
        response = requests.post(f"{config('FEDEX_BASE_API_URL')}/oauth/token", data=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Error authenticating with FedEx API:", e)
        return ValueError("Failed to authenticate with FedEx API")

class FedexTrackingView(APIView):
    def get(self, req):
        try:
            auth_res = auth_fedex()

            # Input data
            data = json.dumps({
                'includeDetailedScans': True,
                'trackingInfo': [
                    {
                        'trackingNumberInfo': {
                            'trackingNumber': "122816215025810"
                        }
                    }
                ]
            })
            headers = {
                'Content-Type': "application/json",
                'X-locale': "en_US",
                'Authorization': "Bearer " + auth_res["access_token"]
            }

            # Make an API call 
            response = requests.post(f"{config('FEDEX_BASE_API_URL')}/track/v1/trackingnumbers", data=data, headers=headers)
            print("API Response Status Code:", response.status_code)  # Debug: Print response status code

            if response.status_code == 200:
                data = response.json()["output"]["completeTrackResults"][0]["trackResults"][0]["scanEvents"]
                
                trackingdetails = [{'eventDescription': event.get('eventDescription',''), 
                                    'city':event.get('scanLocation',{}).get('city','')} for event in data]
                return Response({"Tracking Details": trackingdetails})
            else:
                return Response({"Error": 'Failed to fetch the tracking information'}, status=response.status_code)
        
        except Exception as e:
            print("An error occurred:", e)
            return Response({"Error": "An unexpected error occurred"}, status=500)
