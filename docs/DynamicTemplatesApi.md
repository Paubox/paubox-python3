# paubox.DynamicTemplatesApi

All URIs are relative to *https://api.paubox.net/v1/YOUR_API_USERNAME*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_dynamic_template**](DynamicTemplatesApi.md#create_dynamic_template) | **POST** /dynamic_templates | Create a dynamic template
[**delete_dynamic_template**](DynamicTemplatesApi.md#delete_dynamic_template) | **DELETE** /dynamic_templates/{id} | Delete a dynamic template
[**get_dynamic_template**](DynamicTemplatesApi.md#get_dynamic_template) | **GET** /dynamic_templates/{id} | Get a dynamic template
[**list_dynamic_templates**](DynamicTemplatesApi.md#list_dynamic_templates) | **GET** /dynamic_templates | List all dynamic templates
[**send_templated_message**](DynamicTemplatesApi.md#send_templated_message) | **POST** /templated_messages | Send a dynamically templated message
[**update_dynamic_template**](DynamicTemplatesApi.md#update_dynamic_template) | **PATCH** /dynamic_templates/{id} | Update a dynamic template


# **create_dynamic_template**
> DynamicTemplateResponse create_dynamic_template(data_name, data_body)

Create a dynamic template

Upload a new Handlebars template for dynamic content generation

### Example

* Api Key Authentication (PauboxToken):

```python
import paubox
from paubox.models.dynamic_template_response import DynamicTemplateResponse
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
    api_instance = paubox.DynamicTemplatesApi(api_client)
    data_name = 'data_name_example' # str | Name for the template
    data_body = None # bytearray | Handlebars template file (.hbs)

    try:
        # Create a dynamic template
        api_response = api_instance.create_dynamic_template(data_name, data_body)
        print("The response of DynamicTemplatesApi->create_dynamic_template:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DynamicTemplatesApi->create_dynamic_template: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_name** | **str**| Name for the template | 
 **data_body** | **bytearray**| Handlebars template file (.hbs) | 

### Return type

[**DynamicTemplateResponse**](DynamicTemplateResponse.md)

### Authorization

[PauboxToken](../README.md#PauboxToken)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Template created successfully |  -  |
**400** | Bad request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_dynamic_template**
> DeleteDynamicTemplate200Response delete_dynamic_template(id)

Delete a dynamic template

Delete a specific dynamic template by ID

### Example

* Api Key Authentication (PauboxToken):

```python
import paubox
from paubox.models.delete_dynamic_template200_response import DeleteDynamicTemplate200Response
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
    api_instance = paubox.DynamicTemplatesApi(api_client)
    id = 'id_example' # str | Template ID to delete

    try:
        # Delete a dynamic template
        api_response = api_instance.delete_dynamic_template(id)
        print("The response of DynamicTemplatesApi->delete_dynamic_template:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DynamicTemplatesApi->delete_dynamic_template: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Template ID to delete | 

### Return type

[**DeleteDynamicTemplate200Response**](DeleteDynamicTemplate200Response.md)

### Authorization

[PauboxToken](../README.md#PauboxToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Template deleted successfully |  -  |
**404** | Template not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_dynamic_template**
> DynamicTemplateResponse get_dynamic_template(id)

Get a dynamic template

Retrieve a specific dynamic template by ID

### Example

* Api Key Authentication (PauboxToken):

```python
import paubox
from paubox.models.dynamic_template_response import DynamicTemplateResponse
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
    api_instance = paubox.DynamicTemplatesApi(api_client)
    id = 'id_example' # str | Template ID

    try:
        # Get a dynamic template
        api_response = api_instance.get_dynamic_template(id)
        print("The response of DynamicTemplatesApi->get_dynamic_template:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DynamicTemplatesApi->get_dynamic_template: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Template ID | 

### Return type

[**DynamicTemplateResponse**](DynamicTemplateResponse.md)

### Authorization

[PauboxToken](../README.md#PauboxToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Template details |  -  |
**404** | Template not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_dynamic_templates**
> DynamicTemplateListResponse list_dynamic_templates()

List all dynamic templates

Retrieve all dynamic templates for your organization

### Example

* Api Key Authentication (PauboxToken):

```python
import paubox
from paubox.models.dynamic_template_list_response import DynamicTemplateListResponse
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
    api_instance = paubox.DynamicTemplatesApi(api_client)

    try:
        # List all dynamic templates
        api_response = api_instance.list_dynamic_templates()
        print("The response of DynamicTemplatesApi->list_dynamic_templates:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DynamicTemplatesApi->list_dynamic_templates: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**DynamicTemplateListResponse**](DynamicTemplateListResponse.md)

### Authorization

[PauboxToken](../README.md#PauboxToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of templates |  -  |
**400** | Bad request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **send_templated_message**
> SingleSendResponse send_templated_message(templated_message_request)

Send a dynamically templated message

Send an email using a dynamic template with variable substitution

### Example

* Api Key Authentication (PauboxToken):

```python
import paubox
from paubox.models.single_send_response import SingleSendResponse
from paubox.models.templated_message_request import TemplatedMessageRequest
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
    api_instance = paubox.DynamicTemplatesApi(api_client)
    templated_message_request = {"data":{"template_name":"detailed_test","template_values":"{ \"name\": \"Howard\", \"conditional\":\"true\",\"items\":[\"one\",\"two\",\"three\"] }","message":{"recipients":["recipient@host.com","Recipient Name <recipient2@host.com>"],"bcc":["recipient3@host.com","Recipient Name <recipient4@host.com>"],"headers":{"subject":"sample email","from":"sender@authorized_domain.com","reply-to":"Sender Name <sender@authorized_domain.com>"},"allowNonTLS":false,"forceSecureNotification":false,"attachments":[{"fileName":"hello_world.txt","contentType":"text/plain","content":"SGVsbG8gV29ybGQ"}]}}} # TemplatedMessageRequest | 

    try:
        # Send a dynamically templated message
        api_response = api_instance.send_templated_message(templated_message_request)
        print("The response of DynamicTemplatesApi->send_templated_message:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DynamicTemplatesApi->send_templated_message: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **templated_message_request** | [**TemplatedMessageRequest**](TemplatedMessageRequest.md)|  | 

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
**200** | Templated message sent successfully |  -  |
**400** | Bad request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_dynamic_template**
> DynamicTemplateResponse update_dynamic_template(id, data_name=data_name, data_body=data_body)

Update a dynamic template

Update an existing Handlebars template

### Example

* Api Key Authentication (PauboxToken):

```python
import paubox
from paubox.models.dynamic_template_response import DynamicTemplateResponse
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
    api_instance = paubox.DynamicTemplatesApi(api_client)
    id = 'id_example' # str | Template ID to update
    data_name = 'data_name_example' # str | Updated name for the template (optional)
    data_body = None # bytearray | Updated Handlebars template file (.hbs) (optional)

    try:
        # Update a dynamic template
        api_response = api_instance.update_dynamic_template(id, data_name=data_name, data_body=data_body)
        print("The response of DynamicTemplatesApi->update_dynamic_template:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DynamicTemplatesApi->update_dynamic_template: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Template ID to update | 
 **data_name** | **str**| Updated name for the template | [optional] 
 **data_body** | **bytearray**| Updated Handlebars template file (.hbs) | [optional] 

### Return type

[**DynamicTemplateResponse**](DynamicTemplateResponse.md)

### Authorization

[PauboxToken](../README.md#PauboxToken)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Template updated successfully |  -  |
**400** | Bad request |  -  |
**404** | Template not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

