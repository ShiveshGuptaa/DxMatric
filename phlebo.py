import requests
import datetime
import json
import csv
import smtplib
import io
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


print("Welcome to Dx matrics solver")


# start_date_str = "2024-05-27"
# end_date_str = "2024-06-03"


start_date_str = input("Enter the start date (YYYY-MM-DD): ")
end_date_str = input("Enter the end date (YYYY-MM-DD): ")


Cookie = 'notice_close=true; notice_behavior=implied|eu; ajs_user_id=instanaProduct-63cf686b260c7400016e143a; ajs_anonymous_id=cf0d80ff-f649-4fd5-837b-a9c6df38b1e3; userContext=n/a|0|0|0|IN|KA|1|n/a|implied|zz|n/a|n/a|n/a|n/a; JSESSIONID=dummy; pac4jCsrfToken=8d319290c1b74415aa100070ef501139; in-token=hZKjEtwKTvWW6r_9lkr7XA; INSTANA_JSESSIONID=node0y37bdixco11n14rfk7kka19hs4656.node0; OPTOUTMULTI=0:0%7Cc1:1%7Cc2:0%7Cc3:0; TAsessionID=e7e37530-a8b8-4649-9548-9ae344fd4e95|NEW; ak_bmsc=6E4838512650FECF8CC2124C064E44C4~000000000000000000000000000000~YAAQ1fQ3F6Z/Q1eVAQAAz+tlfxsidVJHpq7usjLM0I/sqCFzrrm1fsf2gKeSD3476myolUeKmMj3CdGfZJEMU6iAvFDbGOr9zianl7SYorjfShSFRLlDXmBWAfCb5qaN35PXRGmI1a01ioo7UikIwXQn7MKAxi1aEsOAmkhpnicXvC34s3FygSBIViFkzFHF1d9KjAuilk8ZVwMX1atRQYH1S0lNGikDq8feoJbZWhEIdffN+eZluFoLQJJhRT4XQT/SSXLQ9l/MZdY5dCShTXgaYc4sKTQjKM9vaN74HbUVcHpYlxjgejTrRYbh0wlmXOoL7KAUZjtvmNkywwsZGUnPknbvIHmHYwjG6+4d1Qs5/a/MX+mslZhbP3OJiKmkkDvSeBuPDr4Jd/xoYHbfpOD+aWw=; utag_main=v_id:0194dfdb75b300033911d61f1c1505075003406d00bd0$_sn:70$_se:38$_ss:0$_st:1741600965840$is_country_requiring_explicit_consent:false$ses_id:1741598817010%3Bexp-session$_pn:1%3Bexp-session; pac4jCsrfToken=0457aeaeb0394cc3b44f33c39e7ae3db; pageviewContext=4618124d-15da-46b3-94d5-ec86b61b28a3'
csrf_url = 'https://consumer-pharmeasy.instana.io/csrf/token'
csrf_headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Cookie': Cookie,
    'Priority': 'u=1, i',
    'Referer': 'https://consumer-pharmeasy.instana.io/',
    'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'X-Instana-L': '1,correlationType=web;correlationId=3876a4ee94a66381',
    'X-Instana-S': '3876a4ee94a66381',
    'X-Instana-T': '3876a4ee94a66381'
}

Dx_Data_response = requests.get(csrf_url, headers=csrf_headers)

csrf_token = None  # Initialize variable a to None
for key, value in Dx_Data_response.headers.items():
    if key == 'x-csrf-token':
        csrf_token = value  # Assign value to a if key is 'x-csrf-token'

if csrf_token is not None:
    print(f"x-csrf-token: {csrf_token}")
else:
    print("csrf-tokes in null")


# take this as input
# start_date_str = "2024-05-19"
# end_date_str = "2024-05-29"
    


start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")

# Calculate timestamps
start_timestamp_ms = int(start_date.timestamp() * 1000)
end_timestamp_ms = int(end_date.timestamp() * 1000)

# Calculate window size in milliseconds
window_size_ms = end_timestamp_ms - start_timestamp_ms

# Construct time frame dictionary
time_frame = {
    "to": end_timestamp_ms,
    "windowSize": window_size_ms,
    "focusedMoment": end_timestamp_ms,
    "autoRefresh": False
}

print("Time Frame:", time_frame)

Dx_Data_url = 'https://consumer-pharmeasy.instana.io/api/application-monitoring/analyze/call-groups'

Dx_Data_headers = {
    'Content-Type': 'application/json',
    'Cookie': Cookie,
    'X-Csrf-Token': csrf_token
}

Dx_Data_Body = {
    "timeFrame":time_frame,
    "tagFilterExpression": {
        "type": "EXPRESSION",
        "logicalOperator": "AND",
        "elements": [
            {
                "type": "EXPRESSION",
                "logicalOperator": "OR",
                "elements": [
                   {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/slot/book-slot"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/slot/availability"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/task/cancel"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/v1/order/reschedule"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/v1/order/manual-assign/{orderId}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/v1/order/hard-assign/{orderId}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/v1/data/available-phlebos"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/task/phlebo-merge-order"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/task/merge-eligble-orders"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/phlebo/calculate-incentive"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/slot/v1/slot-list/{city_id}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "CONTAINS",
            "entity": "DESTINATION",
            "value": "GET /api/slot/v1/slot-info/{Date}/{city_id}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/slot/v1/bulk-slot-list"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/slot/v1/check-slot"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/slot/v1/slots-by-date-range"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/v1/staff/get-cancellation-order"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/v1/staff/get-order-list-today-served"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/v1/staff/get-order-list-myorders"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/v1/staff/get-order-count"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/v1/staff/get-order-list-sot"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/v1/staff/get-order-list-myappointment"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/v1/data/visit-details-by-btechid/{btechId}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/slot/v1/phlebo-available-slot"
          }
                ]
            }
        ]
    },
    "metrics": [
        {
            "metric": "calls",
            "aggregation": "SUM"
        },
        {
            "metric": "erroneousCalls",
            "aggregation": "SUM"
        },
        {
            "metric": "errors",
            "aggregation": "MEAN"
        },
        {
            "metric": "latency",
            "aggregation": "MEAN"
        },
        {
            "metric": "latency",
            "aggregation": "P95"
        }
    ],
    "order": {
        "by": "timestamp",
        "direction": "DESC"
    },
    "group": {
        "groupbyTag": "endpoint.name",
        "groupbyTagEntity": "DESTINATION"
    }
}

Dx_Data_response = requests.post(Dx_Data_url, headers=Dx_Data_headers, json=Dx_Data_Body)

Dx_parsed_data = Dx_Data_response.json()

# Initialize an empty dictionary to store rows
array = {}

for item in Dx_parsed_data.get('items', []):
    name = item['name']
    calls_sum = round(item['metrics']['calls.sum'][0][1])
    latency_mean = round(item['metrics']['latency.mean'][0][1])
    latency_p95 = round(item['metrics']['latency.p95'][0][1])
    
    # Initialize the dictionary for this name if not already initialized
    if name not in array:
        array[name] = {}
    
    # Update the dictionary with counts and averages
    array[name]['count'] = calls_sum
    array[name]['avg'] = latency_mean
    array[name]['p95'] = latency_p95
    array[name]['5xx'] = 0
    array[name]['4xx'] = 0


url = "https://consumer-pharmeasy.instana.io/api/application-monitoring/analyze/call-groups"

headers = {
    "Content-Type": "application/json",
    "Cookie": Cookie,
    "X-Csrf-Token": csrf_token
}


error_5xx_body ={
  "timeFrame": time_frame,
  "tagFilterExpression": {
    "type": "EXPRESSION",
    "logicalOperator": "AND",
    "elements": [
      {
        "type": "TAG_FILTER",
        "name": "call.http.statusClass",
        "operator": "EQUALS",
        "entity": "NOT_APPLICABLE",
        "value": "5xx"
      },
      {
        "type": "EXPRESSION",
        "logicalOperator": "OR",
       "elements": [
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/slot/book-slot"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/slot/availability"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/task/cancel"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/v1/order/reschedule"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/v1/order/manual-assign/{orderId}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/v1/order/hard-assign/{orderId}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/v1/data/available-phlebos"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/task/phlebo-merge-order"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/task/merge-eligble-orders"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/phlebo/calculate-incentive"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/slot/v1/slot-list/{city_id}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "CONTAINS",
            "entity": "DESTINATION",
            "value": "GET /api/slot/v1/slot-info/{Date}/{city_id}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/slot/v1/bulk-slot-list"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/slot/v1/check-slot"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/slot/v1/slots-by-date-range"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/v1/staff/get-cancellation-order"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/v1/staff/get-order-list-today-served"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/v1/staff/get-order-list-myorders"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/v1/staff/get-order-count"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/v1/staff/get-order-list-sot"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/v1/staff/get-order-list-myappointment"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/v1/data/visit-details-by-btechid/{btechId}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/slot/v1/phlebo-available-slot"
          }
        ]
      }
    ]
  },
  "metrics": [
    {
      "metric": "calls",
      "aggregation": "SUM"
    },
    {
      "metric": "errors",
      "aggregation": "MEAN"
    }
  ],
  "order": {
    "by": "timestamp",
    "direction": "DESC"
  },
  "group": {
    "groupbyTag": "endpoint.name",
    "groupbyTagEntity": "DESTINATION"
  }
}

Dx_Data_response = requests.post(Dx_Data_url, headers=Dx_Data_headers, json=error_5xx_body)

Dx_5xx_data = Dx_Data_response.json()

for item in Dx_5xx_data.get('items', []):
    name = item['name']
    calls_sum = round(item['metrics']['calls.sum'][0][1])

    if name not in array:
        array[name] = {}

    array[name]['5xx'] = calls_sum


error_4xx_body = {
   "timeFrame": time_frame,
  "tagFilterExpression": {
    "type": "EXPRESSION",
    "logicalOperator": "AND",
    "elements": [
      {
        "type": "TAG_FILTER",
        "name": "call.http.statusClass",
        "operator": "EQUALS",
        "entity": "NOT_APPLICABLE",
        "value": "4xx"
      },
      {
        "type": "EXPRESSION",
        "logicalOperator": "OR",
       "elements": [
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/slot/book-slot"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/slot/availability"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/task/cancel"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/v1/order/reschedule"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/v1/order/manual-assign/{orderId}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/v1/order/hard-assign/{orderId}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/v1/data/available-phlebos"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/task/phlebo-merge-order"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/task/merge-eligble-orders"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/phlebo/calculate-incentive"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/slot/v1/slot-list/{city_id}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "CONTAINS",
            "entity": "DESTINATION",
            "value": "GET /api/slot/v1/slot-info/{Date}/{city_id}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/slot/v1/bulk-slot-list"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/slot/v1/check-slot"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/slot/v1/slots-by-date-range"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/v1/staff/get-cancellation-order"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/v1/staff/get-order-list-today-served"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/v1/staff/get-order-list-myorders"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/v1/staff/get-order-count"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/v1/staff/get-order-list-sot"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/v1/staff/get-order-list-myappointment"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/v1/data/visit-details-by-btechid/{btechId}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/slot/v1/phlebo-available-slot"
          }
        ]
      }
    ]
  },
  "metrics": [
    {
      "metric": "calls",
      "aggregation": "SUM"
    },
    {
      "metric": "errors",
      "aggregation": "MEAN"
    }
  ],
  "order": {
    "by": "timestamp",
    "direction": "DESC"
  },
  "group": {
    "groupbyTag": "endpoint.name",
    "groupbyTagEntity": "DESTINATION"
  }
}

Dx_Data_response = requests.post(Dx_Data_url, headers=Dx_Data_headers, json=error_4xx_body)

Dx_4xx_data = Dx_Data_response.json()

for item in Dx_4xx_data.get('items', []):
    name = item['name']
    calls_sum = round(item['metrics']['calls.sum'][0][1])

    if name not in array:
        array[name] = {}

    array[name]['4xx'] = calls_sum


Dx_Endpoints_Order = [
   'POST /api/slot/book-slot',
   'GET /api/slot/availability',
   'POST /api/task/cancel',
   'POST /api/v1/order/reschedule',
   'POST /api/v1/order/manual-assign/{orderId}',
   'POST /api/v1/order/hard-assign/{orderId}',
   'GET /api/v1/data/available-phlebos',
   'POST /api/task/phlebo-merge-order',
   'GET /api/task/merge-eligble-orders',
   'POST /api/phlebo/calculate-incentive',
   'GET /api/slot/v1/slot-list/{city_id}',
   'GET /api/slot/v1/slot-info/{Date}/{city_id}',
   'POST /api/slot/v1/bulk-slot-list',
   'GET /api/slot/v1/check-slot',
   'GET /api/slot/v1/slots-by-date-range',
   'GET /api/v1/staff/get-cancellation-order',
   'GET /api/v1/staff/get-order-list-today-served',
   'GET /api/v1/staff/get-order-list-myorders',
   'GET /api/v1/staff/get-order-count',
   'GET /api/v1/staff/get-order-list-sot',
   'GET /api/v1/staff/get-order-list-myappointment',
   'GET /api/v1/data/visit-details-by-btechid/{btechId}',
   'GET /api/slot/v1/phlebo-available-slot'
]


# for val in Dx_Endpoints_Order:
#     if val not in array:
#         print('null api', {val})
#     else:
#          print(f"{val}: {array[val]}")
  
# for key, value in array.items():
#     print(f"{key}: {value}")

    



# Convert the nested dictionary to CSV format in a string
output = io.StringIO()
csv_writer = csv.writer(output)
csv_writer.writerow(['API','Count','Mean', 'P95', '5xx', '4xx'])  # Write header
for val in Dx_Endpoints_Order:
    value = array[val]
    csv_writer.writerow([val,value['count'],value['avg'], value['p95'], value['5xx'], value['4xx']])
csv_data = output.getvalue()
output.close()


print(csv_data)


# Email configuration
from_email = 'sindhu.madakasira@pharmeasy.in'
to_email = 'oxygen-dev@pharmeasy.in, sindhu.madakasira@pharmeasy.in'
subject = f'Oxygen Diag API Metrics: {start_date_str} to {end_date_str}'
body = f'Please find the data below in CSV format:\n\n{csv_data}'
smtp_server = 'smtp.gmail.com'
smtp_port = 587
username = 'sindhu.madakasira@pharmeasy.in'
password = 'lanu ksds cjpr tkqb'

# Create the email
msg = MIMEMultipart() 
msg['From'] = from_email
msg['To'] = to_email
msg['Subject'] = subject

# Attach the body of the email with CSV data
msg.attach(MIMEText(body, 'plain'))

# Send the email
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(username, password)
    server.send_message(msg)
    server.quit()
    print('Email sent successfully.')
except Exception as e:
    print(f'Failed to send email: {e}')
