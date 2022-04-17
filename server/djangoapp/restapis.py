import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth

def get_request(url, **kwargs):
    # print(kwargs)
    print("GET from {} ".format(url))
    try:
        api_key = kwargs.get('api_key')
        if api_key:
            #set params
            params=dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key), params=params)
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)

    except:
        # If any error occurs
        print("Network exception occurred")
        raise ValueError("Network exception occurred.")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    # print(json_data)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

def post_request(url, json_payload, **kwargs):
    print("POST to {} ".format(url))
    try:
        response = requests.post(
            url, params=kwargs, json=json_payload,
            headers={'Content-Type': 'application/json'}
        )
    except:
        # If any error occurs
        print("Network exception occurred")
        raise ValueError("Network exception occurred.")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    return response.content


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealerships"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                address = dealer.get("address", ""),
                city = dealer.get("city", ""),
                full_name = dealer.get("full_name", ""),
                id = dealer.get("id", ""),
                lat = dealer.get("lat", ""),
                long = dealer.get("long", ""),
                short_name = dealer.get("short_name", ""),
                st=dealer.get("st", ""),
                zip = dealer.get("zip", ""))
            results.append(dealer_obj)

    return results

# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_by_id(url, dealerId, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealerships"]
        # For each dealer object
        for dealer in dealers:
            dealer_id = dealer.get("id", -1)
            if dealer_id == dealerId:
                # Create a CarDealer object with values in `doc` object
                dealer_obj = CarDealer(
                    address = dealer.get("address", ""),
                    city = dealer.get("city", ""),
                    full_name = dealer.get("full_name", ""),
                    id = dealer.get("id", ""),
                    lat = dealer.get("lat", ""),
                    long = dealer.get("long", ""),
                    short_name = dealer.get("short_name", ""),
                    st=dealer.get("st", ""),
                    zip = dealer.get("zip", ""))
                results.append(dealer_obj)
    if len(results) > 0:
        return results[0]
    else:
        return []

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_reviews_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        if json_result['code']:
            if json_result['code'] == 404:
                print('dealerId does not exist.')
                return []
        
        # Get the row list in JSON as reviews
        reviews = json_result["data"]
        # For each review object
        for review in reviews:
            
            # Create a CarDealer object with values in `review` object
            review_obj = DealerReview(
                # dealership, name, review, car_make, car_model, car_year, sentiment, id
                dealership = review.get("dealership", ""),
                reviewer_name = review.get("name", ""),
                review = review.get("review", ""),
                purchase = review.get('purchase', False),
                purchase_date = review.get("purchase_date", ""),
                car_make = review.get("car_make", ""),
                car_model = review.get("car_model", ""),
                car_year = review.get("car_year", ""),
                sentiment = "",
                id=review.get("id", ""))
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

from cfenv import AppEnv
env = AppEnv()
nlu = env.get_service(label='natural-language-understanding')

nlu_creds = nlu.credentials
nlu_apikey = nlu_creds['apikey']
nlu_url = nlu_creds['url'] + '/v1/analyze'

def analyze_review_sentiments(dealerreview):
    result = get_request(
        nlu_url,
        api_key=nlu_apikey,
        text=dealerreview,
        version='2021-08-01',
        features='sentiment',
        return_analyzed_text=False
    )
    if 'code' in result.keys():
        if result['code'] == 422:
            return 'neutral'
    
    return result['sentiment']['document']['label']

