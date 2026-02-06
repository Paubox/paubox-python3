# TemplatedMessageRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**TemplatedMessageRequestData**](TemplatedMessageRequestData.md) |  | 

## Example

```python
from paubox.models.templated_message_request import TemplatedMessageRequest

# TODO update the JSON string below
json = "{}"
# create an instance of TemplatedMessageRequest from a JSON string
templated_message_request_instance = TemplatedMessageRequest.from_json(json)
# print the JSON string representation of the object
print(TemplatedMessageRequest.to_json())

# convert the object into a dict
templated_message_request_dict = templated_message_request_instance.to_dict()
# create an instance of TemplatedMessageRequest from a dict
templated_message_request_from_dict = TemplatedMessageRequest.from_dict(templated_message_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


