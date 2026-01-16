# TemplatedMessageRequestData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**template_name** | **str** | The name of the template to use (must match exactly) | 
**template_values** | **str** | JSON-formatted string containing template variable values | 
**message** | [**TemplatedMessage**](TemplatedMessage.md) |  | 

## Example

```python
from paubox.models.templated_message_request_data import TemplatedMessageRequestData

# TODO update the JSON string below
json = "{}"
# create an instance of TemplatedMessageRequestData from a JSON string
templated_message_request_data_instance = TemplatedMessageRequestData.from_json(json)
# print the JSON string representation of the object
print(TemplatedMessageRequestData.to_json())

# convert the object into a dict
templated_message_request_data_dict = templated_message_request_data_instance.to_dict()
# create an instance of TemplatedMessageRequestData from a dict
templated_message_request_data_from_dict = TemplatedMessageRequestData.from_dict(templated_message_request_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


