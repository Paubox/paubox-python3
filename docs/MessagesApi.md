# paubox.MessagesApi

All URIs are relative to *https://api.paubox.net/v1/YOUR_API_USERNAME*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_message_receipt**](MessagesApi.md#get_message_receipt) | **GET** /message_receipt | Get email disposition
[**send_bulk_messages**](MessagesApi.md#send_bulk_messages) | **POST** /bulk_messages | Send multiple email messages (batch)
[**send_message**](MessagesApi.md#send_message) | **POST** /messages | Send a single email message


# **get_message_receipt**
> MessageReceiptResponse get_message_receipt(source_tracking_id)

Get email disposition

Retrieve delivery status, open tracking, and click tracking information for a sent message

### Example

* Api Key Authentication (PauboxToken):

```python
import paubox
from paubox.models.message_receipt_response import MessageReceiptResponse
from paubox.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.paubox.net/v1/YOUR_API_USERNAME
# See configuration.py for a list of all supported configuration parameters.
configuration = paubox.Configuration(
    host = "https://api.paubox.net/v1/YOUR_API_USERNAME"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: PauboxToken
configuration.api_key['PauboxToken'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['PauboxToken'] = 'Bearer'

# Enter a context with an instance of the API client
with paubox.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = paubox.MessagesApi(api_client)
    source_tracking_id = UUID('6e1cf9a4-7bde-4834-8200-ed424b50c8a7') # UUID | The tracking ID returned when the message was sent

    try:
        # Get email disposition
        api_response = api_instance.get_message_receipt(source_tracking_id)
        print("The response of MessagesApi->get_message_receipt:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MessagesApi->get_message_receipt: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **source_tracking_id** | **UUID**| The tracking ID returned when the message was sent | 

### Return type

[**MessageReceiptResponse**](MessageReceiptResponse.md)

### Authorization

[PauboxToken](../README.md#PauboxToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Message disposition data |  -  |
**404** | Message not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **send_bulk_messages**
> BulkSendResponse send_bulk_messages(bulk_send_request)

Send multiple email messages (batch)

Sends multiple messages in one request. Paubox recommends batches of 50 or fewer. Source tracking IDs are returned in the same order as the messages array.


### Example

* Api Key Authentication (PauboxToken):

```python
import paubox
from paubox.models.bulk_send_request import BulkSendRequest
from paubox.models.bulk_send_response import BulkSendResponse
from paubox.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.paubox.net/v1/YOUR_API_USERNAME
# See configuration.py for a list of all supported configuration parameters.
configuration = paubox.Configuration(
    host = "https://api.paubox.net/v1/YOUR_API_USERNAME"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: PauboxToken
configuration.api_key['PauboxToken'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['PauboxToken'] = 'Bearer'

# Enter a context with an instance of the API client
with paubox.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = paubox.MessagesApi(api_client)
    bulk_send_request = {"data":{"messages":[{"recipients":["recipient@host.com","Recipient Name <recipient@host.com>"],"bcc":["recipient3@host.com","Recipient Name <recipient4@host.com>"],"headers":{"subject":"sample email","from":"sender@authorized_domain.com","reply-to":"Sender Name <sender@authorized_domain.com>","x-custom-header":"sample custom header"},"content":{"text/plain":"Hello World!","text/html":"<html><body><h1>Hello World!</h1></body></html>"},"attachments":[{"fileName":"hello_world.txt","contentType":"text/plain","content":"SGVsbG8gV29ybGQh"}],"allowNonTLS":false,"forceSecureNotification":false},{"recipients":["recipient2@host.com","Recipient Name <recipient2@host.com>"],"headers":{"subject":"sample email","from":"sender@authorized_domain.com","reply-to":"Sender Name <sender@authorized_domain.com>"},"content":{"text/plain":"Hello World!","text/html":"<html><body><h1>Hello World!</h1></body></html>"},"attachments":[{"fileName":"hello_world.txt","contentType":"text/plain","content":"SGVsbG8gV29ybGQh"}]}]}} # BulkSendRequest | 

    try:
        # Send multiple email messages (batch)
        api_response = api_instance.send_bulk_messages(bulk_send_request)
        print("The response of MessagesApi->send_bulk_messages:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MessagesApi->send_bulk_messages: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bulk_send_request** | [**BulkSendRequest**](BulkSendRequest.md)|  | 

### Return type

[**BulkSendResponse**](BulkSendResponse.md)

### Authorization

[PauboxToken](../README.md#PauboxToken)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Batch accepted |  -  |
**400** | Bad request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **send_message**
> SingleSendResponse send_message(single_send_request)

Send a single email message

### Example

* Api Key Authentication (PauboxToken):

```python
import paubox
from paubox.models.single_send_request import SingleSendRequest
from paubox.models.single_send_response import SingleSendResponse
from paubox.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.paubox.net/v1/YOUR_API_USERNAME
# See configuration.py for a list of all supported configuration parameters.
configuration = paubox.Configuration(
    host = "https://api.paubox.net/v1/YOUR_API_USERNAME"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: PauboxToken
configuration.api_key['PauboxToken'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['PauboxToken'] = 'Bearer'

# Enter a context with an instance of the API client
with paubox.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = paubox.MessagesApi(api_client)
    single_send_request = {"data":{"message":{"recipients":["recipient@host.com"],"headers":{"subject":"Hello from the Paubox Email API","from":"sender@verifieddomain.com"},"content":{"text/plain":"Hello world","text/html":"<html><body><h1>Hello world</h1></body></html>"}}}} # SingleSendRequest | 

    try:
        # Send a single email message
        api_response = api_instance.send_message(single_send_request)
        print("The response of MessagesApi->send_message:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MessagesApi->send_message: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **single_send_request** | [**SingleSendRequest**](SingleSendRequest.md)|  | 

### Return type

[**SingleSendResponse**](SingleSendResponse.md)

### Authorization

[PauboxToken](../README.md#PauboxToken)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Message accepted |  -  |
**400** | Bad request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

