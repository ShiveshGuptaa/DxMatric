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


Cookie = 'ajs_anonymous_id=a570ac24-e7e3-4ffa-80bf-3e9954a91b2e; INSTANA_JSESSIONID=node014epqt00i3zlh1xqawy9c10som279037.node0; in-token=tMI428MNSgyfOS86-eDtuQ; pac4jCsrfToken=914763dfc44342af988db2d757314b0c; JSESSIONID=dummy'
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
                        "value": "GET /techso/v1/api/ordervisitdetailsoptimize/getordervisitdetailsorderwise"
                    },
                    {
                        "type": "TAG_FILTER",
                        "name": "endpoint.name",
                        "operator": "EQUALS",
                        "entity": "DESTINATION",
                        "value": "POST /techso/v1/api/woe"
                    },
                    {
                        "type": "TAG_FILTER",
                        "name": "endpoint.name",
                        "operator": "EQUALS",
                        "entity": "DESTINATION",
                        "value": "GET /techso/v1/api/orderdetailsbyvisit/{orderid}"
                    },
                    {
                        "type": "TAG_FILTER",
                        "name": "endpoint.name",
                        "operator": "EQUALS",
                        "entity": "DESTINATION",
                        "value": "POST /techso/v1/api/peevents/peorderedit"
                    },
                    {
                        "type": "TAG_FILTER",
                        "name": "endpoint.name",
                        "operator": "EQUALS",
                        "entity": "DESTINATION",
                        "value": "POST /techso/v1/api/peevents/peupdatepatient"
                    },
                    {
                        "type": "TAG_FILTER",
                        "name": "endpoint.name",
                        "operator": "EQUALS",
                        "entity": "DESTINATION",
                        "value": "POST /techso/v1/api/orderallocation/ordereditdetails"
                    },
                    {
                        "type": "TAG_FILTER",
                        "name": "endpoint.name",
                        "operator": "EQUALS",
                        "entity": "DESTINATION",
                        "value": "POST /techso/v1/api/createpatient/phlebo"
                    },
                    {
                        "type": "TAG_FILTER",
                        "name": "endpoint.name",
                        "operator": "EQUALS",
                        "entity": "DESTINATION",
                        "value": "POST /techso/v1/api/orderallocation/uploadblob"
                    },
                    {
                        "type": "TAG_FILTER",
                        "name": "endpoint.name",
                        "operator": "EQUALS",
                        "entity": "DESTINATION",
                        "value": "GET /api/order/details/{orderId}"
                    },
                    {
                        "type": "TAG_FILTER",
                        "name": "endpoint.name",
                        "operator": "EQUALS",
                        "entity": "DESTINATION",
                        "value": "GET /api/order/ben-details/{orderId}"
                    },
                    {
                        "type": "TAG_FILTER",
                        "name": "endpoint.name",
                        "operator": "EQUALS",
                        "entity": "DESTINATION",
                        "value": "GET /api/order/ben-test-details/{orderId}"
                    },
                    {
                        "type": "TAG_FILTER",
                        "name": "endpoint.name",
                        "operator": "CONTAINS",
                        "entity": "DESTINATION",
                        "value": "GET /api/order/booking-ben-test-details/{orderId}"
                    },
                    {
                        "type": "TAG_FILTER",
                        "name": "endpoint.name",
                        "operator": "EQUALS",
                        "entity": "DESTINATION",
                        "value": "POST /api/order/add-ben"
                    },
                    {
                        "type": "TAG_FILTER",
                        "name": "endpoint.name",
                        "operator": "EQUALS",
                        "entity": "DESTINATION",
                        "value": "PUT /api/order/edit-ben"
                    },
                    {
                        "type": "TAG_FILTER",
                        "name": "endpoint.name",
                        "operator": "EQUALS",
                        "entity": "DESTINATION",
                        "value": "DELETE /api/order/remove-ben/{orderId}"
                    },
                    {
                        "type": "TAG_FILTER",
                        "name": "endpoint.name",
                        "operator": "EQUALS",
                        "entity": "DESTINATION",
                        "value": "GET /api/reports/getpatientreport"
                    },
                    {
                        "type": "TAG_FILTER",
                        "name": "endpoint.name",
                        "operator": "EQUALS",
                        "entity": "DESTINATION",
                        "value": "POST /api/order/update-status/{orderId}"
                    },
                    {
                        "type": "TAG_FILTER",
                        "name": "endpoint.name",
                        "operator": "EQUALS",
                        "entity": "DESTINATION",
                        "value": "GET /sample-details"
                    },
                    {
                        "type": "TAG_FILTER",
                        "name": "endpoint.name",
                        "operator": "EQUALS",
                        "entity": "DESTINATION",
                        "value": "GET /report-page-details/{id}"
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
            "value": "GET /techso/v1/api/ordervisitdetailsoptimize/getordervisitdetailsorderwise"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /techso/v1/api/woe"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /techso/v1/api/orderdetailsbyvisit/{orderid}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /techso/v1/api/peevents/peorderedit"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /techso/v1/api/peevents/peupdatepatient"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /techso/v1/api/orderallocation/ordereditdetails"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /techso/v1/api/createpatient/phlebo"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /techso/v1/api/orderallocation/uploadblob"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/order/details/{orderId}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/order/ben-details/{orderId}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/order/ben-test-details/{orderId}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "CONTAINS",
            "entity": "DESTINATION",
            "value": "GET /api/order/booking-ben-test-details/{orderId}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/order/add-ben"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "PUT /api/order/edit-ben"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "DELETE /api/order/remove-ben/{orderId}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/reports/getpatientreport"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/order/update-status/{orderId}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /sample-details"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /report-page-details/{id}"
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
            "value": "GET /techso/v1/api/ordervisitdetailsoptimize/getordervisitdetailsorderwise"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /techso/v1/api/woe"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /techso/v1/api/orderdetailsbyvisit/{orderid}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /techso/v1/api/peevents/peorderedit"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /techso/v1/api/peevents/peupdatepatient"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /techso/v1/api/orderallocation/ordereditdetails"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /techso/v1/api/createpatient/phlebo"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /techso/v1/api/orderallocation/uploadblob"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/order/details/{orderId}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/order/ben-details/{orderId}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/order/ben-test-details/{orderId}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "CONTAINS",
            "entity": "DESTINATION",
            "value": "GET /api/order/booking-ben-test-details/{orderId}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/order/add-ben"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "PUT /api/order/edit-ben"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "DELETE /api/order/remove-ben/{orderId}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /api/reports/getpatientreport"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "POST /api/order/update-status/{orderId}"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /sample-details"
          },
          {
            "type": "TAG_FILTER",
            "name": "endpoint.name",
            "operator": "EQUALS",
            "entity": "DESTINATION",
            "value": "GET /report-page-details/{id}"
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
    'GET /techso/v1/api/ordervisitdetailsoptimize/getordervisitdetailsorderwise',
    'GET /techso/v1/api/orderdetailsbyvisit/{orderid}',
    'POST /techso/v1/api/woe',
    'POST /techso/v1/api/peevents/peupdatepatient',
    'POST /techso/v1/api/orderallocation/ordereditdetails',
    'POST /techso/v1/api/createpatient/phlebo',
    'POST /techso/v1/api/peevents/peorderedit',
    'GET /api/order/details/{orderId}',
    'GET /api/order/ben-details/{orderId}',
    'GET /api/order/ben-test-details/{orderId}',
    'POST /api/order/add-ben',
    'PUT /api/order/edit-ben',
    'DELETE /api/order/remove-ben/{orderId}',
    'GET /api/order/booking-ben-test-details/{orderId}',
    'GET /api/reports/getpatientreport',
    'POST /api/order/update-status/{orderId}',
    'POST /techso/v1/api/orderallocation/uploadblob',
    'GET /sample-details',
    'GET /report-page-details/{id}'
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
from_email = 'shivesh.kumar@pharmeasy.in'
to_email = 'oxygen-dev@pharmeasy.in'
subject = f'Oxygen Diag API Metrics: {start_date_str} to {end_date_str}'
body = f'Please find the data below in CSV format:\n\n{csv_data}'
smtp_server = 'smtp.gmail.com'
smtp_port = 587
username = 'shivesh.kumar@pharmeasy.in'
password = '***change'

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
