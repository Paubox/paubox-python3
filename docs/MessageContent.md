# MessageContent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**text_plain** | **str** | Plain text message body. Required if text/html is not provided. | [optional] 
**text_html** | **str** | HTML message body. May be HTML-escaped, base64-encoded, or a valid unescaped string. CSS in &lt;style&gt; tags will be rendered inline.  | [optional] 

## Example

```python
from paubox.models.message_content import MessageContent

# TODO update the JSON string below
json = "{}"
# create an instance of MessageContent from a JSON string
message_content_instance = MessageContent.from_json(json)
# print the JSON string representation of the object
print(MessageContent.to_json())

# convert the object into a dict
message_content_dict = message_content_instance.to_dict()
# create an instance of MessageContent from a dict
message_content_from_dict = MessageContent.from_dict(message_content_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


