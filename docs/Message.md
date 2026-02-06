# Message


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**recipients** | **List[str]** |  | 
**bcc** | **List[str]** |  | [optional] 
**cc** | **List[str]** |  | [optional] 
**headers** | [**MessageHeaders**](MessageHeaders.md) |  | 
**allow_non_tls** | **bool** | Allow delivery over non-TLS rather than converting to a Secure Portal message. Not HIPAA-compliant if the message contains PHI.  | [optional] [default to False]
**force_secure_notification** | **bool** | Force delivery as a Paubox Secure Message; recipient gets a pickup notification with a link.  | [optional] [default to False]
**content** | [**MessageContent**](MessageContent.md) |  | 
**attachments** | [**List[Attachment]**](Attachment.md) |  | [optional] 

## Example

```python
from paubox.models.message import Message

# TODO update the JSON string below
json = "{}"
# create an instance of Message from a JSON string
message_instance = Message.from_json(json)
# print the JSON string representation of the object
print(Message.to_json())

# convert the object into a dict
message_dict = message_instance.to_dict()
# create an instance of Message from a dict
message_from_dict = Message.from_dict(message_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


