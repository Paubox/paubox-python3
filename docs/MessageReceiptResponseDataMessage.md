# MessageReceiptResponseDataMessage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The message ID | 
**message_deliveries** | [**List[MessageDelivery]**](MessageDelivery.md) |  | 
**total_opens** | **int** | Total number of opens (single recipient only) | [optional] 
**distinct_opens** | **int** | Number of distinct opens (single recipient only) | [optional] 
**total_click_count** | **int** | Total number of clicks (single recipient only) | [optional] 
**clicks_per_link** | [**List[ClickData]**](ClickData.md) | Click tracking data per link (single recipient only) | [optional] 
**unsubscribed** | **bool** | Whether the recipient has unsubscribed (single recipient only) | [optional] 

## Example

```python
from paubox.models.message_receipt_response_data_message import MessageReceiptResponseDataMessage

# TODO update the JSON string below
json = "{}"
# create an instance of MessageReceiptResponseDataMessage from a JSON string
message_receipt_response_data_message_instance = MessageReceiptResponseDataMessage.from_json(json)
# print the JSON string representation of the object
print(MessageReceiptResponseDataMessage.to_json())

# convert the object into a dict
message_receipt_response_data_message_dict = message_receipt_response_data_message_instance.to_dict()
# create an instance of MessageReceiptResponseDataMessage from a dict
message_receipt_response_data_message_from_dict = MessageReceiptResponseDataMessage.from_dict(message_receipt_response_data_message_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


