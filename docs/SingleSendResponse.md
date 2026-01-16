# SingleSendResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**source_tracking_id** | **str** | Identifier for tracking the message source. | [optional] 
**custom_headers** | **Dict[str, str]** |  | [optional] 
**data** | **str** |  | [optional] 

## Example

```python
from paubox.models.single_send_response import SingleSendResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SingleSendResponse from a JSON string
single_send_response_instance = SingleSendResponse.from_json(json)
# print the JSON string representation of the object
print(SingleSendResponse.to_json())

# convert the object into a dict
single_send_response_dict = single_send_response_instance.to_dict()
# create an instance of SingleSendResponse from a dict
single_send_response_from_dict = SingleSendResponse.from_dict(single_send_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


