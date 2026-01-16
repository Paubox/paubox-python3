# SingleSendRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**SingleSendRequestData**](SingleSendRequestData.md) |  | 

## Example

```python
from paubox.models.single_send_request import SingleSendRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SingleSendRequest from a JSON string
single_send_request_instance = SingleSendRequest.from_json(json)
# print the JSON string representation of the object
print(SingleSendRequest.to_json())

# convert the object into a dict
single_send_request_dict = single_send_request_instance.to_dict()
# create an instance of SingleSendRequest from a dict
single_send_request_from_dict = SingleSendRequest.from_dict(single_send_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


