# TemplatedMessage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**recipients** | **List[str]** |  | 
**bcc** | **List[str]** |  | [optional] 
**cc** | **List[str]** |  | [optional] 
**headers** | [**TemplatedMessageHeaders**](TemplatedMessageHeaders.md) |  | 
**allow_non_tls** | **bool** | Allow delivery over non-TLS rather than converting to a Secure Portal message. Not HIPAA-compliant if the message contains PHI.  | [optional] [default to False]
**force_secure_notification** | **bool** | Force delivery as a Paubox Secure Message; recipient gets a pickup notification with a link.  | [optional] [default to False]
**attachments** | [**List[Attachment]**](Attachment.md) |  | [optional] 

## Example

```python
from paubox.models.templated_message import TemplatedMessage

# TODO update the JSON string below
json = "{}"
# create an instance of TemplatedMessage from a JSON string
templated_message_instance = TemplatedMessage.from_json(json)
# print the JSON string representation of the object
print(TemplatedMessage.to_json())

# convert the object into a dict
templated_message_dict = templated_message_instance.to_dict()
# create an instance of TemplatedMessage from a dict
templated_message_from_dict = TemplatedMessage.from_dict(templated_message_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


