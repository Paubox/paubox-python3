# MessageDelivery


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**recipient** | **str** | The recipient email address | 
**status** | [**DeliveryStatus**](DeliveryStatus.md) |  | 

## Example

```python
from paubox.models.message_delivery import MessageDelivery

# TODO update the JSON string below
json = "{}"
# create an instance of MessageDelivery from a JSON string
message_delivery_instance = MessageDelivery.from_json(json)
# print the JSON string representation of the object
print(MessageDelivery.to_json())

# convert the object into a dict
message_delivery_dict = message_delivery_instance.to_dict()
# create an instance of MessageDelivery from a dict
message_delivery_from_dict = MessageDelivery.from_dict(message_delivery_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


