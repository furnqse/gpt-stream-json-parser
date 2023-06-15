# force_parse_json

`force_parse_json` is a Python function designed to handle incomplete or 'partial' JSON strings. It first tries to 'close' or complete the JSON, then attempts to parse it. If the parsing is successful, it optionally cleans up the resulting Python dictionary before returning it.

If parsing fails, the function either returns `None` or prints an error message, depending on the parameters you specify. 

## Usage

```python
from gpt_stream_parser import force_parse_json

output = ""
for chunk in response:
    output += chunk.choices[0].delta.function_call.arguments
    data = force_parse_json(output)
    if data:
        print(data)
```

### Parameters

- `partial_json` (str): The incomplete JSON string.
- `report_error` (bool, optional): If set to `True`, any exceptions that occur during parsing will be printed to the console. If `False`, they will be ignored. Default is `False`.
- `clean_up` (bool, optional): If set to `True`, the resulting Python dictionary will be 'cleaned up' before it is returned. If `False`, the function will return the dictionary as is. Default is `True`.

### Returns

- `dict` or `None`: The function returns the parsed JSON as a Python dictionary if successful. If an error occurs during parsing, it returns `None`.

### Example

This example uses the `force_parse_json` function in the context of streaming API responses. It uses the OpenAI GPT-3.5 model to obtain chat completions, which are streamed in chunks. The function attempts to parse the data contained in each chunk and print it to the console.

```python
import openai
from gpt_stream_parser import force_parse_json

# create a chat completion
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[{"role": "user", "content": "What's the weather like in Boston?"}],
    functions=[
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        }
    ],
    function_call="auto",
    stream=True,
)

# parse and print the data contained in each chunk
output = ""
for chunk in response:
    output += chunk.choices[0].delta.function_call.arguments
    data = force_parse_json(output)
    if data:
        print(data)
```
In this example, `force_parse_json` is used to parse the data contained in each chunk of the response. The parsed data is then printed to the console. Note that this function is useful for handling streaming API responses, where data may be received in incomplete 'chunks'.