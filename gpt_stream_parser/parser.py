import json

opening_braces = ['[', '{', '"']
closing_braces = [']', '}', '"']
common_braces = ['"']
open_to_close = { k: v for k, v in zip(opening_braces, closing_braces)}
close_to_open = { k: v for k, v in zip(closing_braces, opening_braces)}

# jsonの部分文字列を受け取って、閉じられたjson文字列を返す
# 例: close_partial_json('{"foo": ["bar", "baz"]') == '{"foo": ["bar", "baz"]}'
# Mapのキーの途中で終了している場合は、正常なJSONを返さない
def close_partial_json(partial_json):
    stack = []
    for char in partial_json:
        if char in common_braces:
            if stack and stack[-1] == char:
                stack.pop()
            else:
                stack.append(char)
        elif stack and stack[-1] in common_braces:
            continue
        elif char in opening_braces:
            stack.append(char)
        elif char in closing_braces:
            if stack[-1] == close_to_open[char]:
                stack.pop()
            else:
                raise ValueError("Invalid JSON: missing opening brace for " + char)
    closed_json = partial_json
    for unclosed_brace in reversed(stack):
        closed_json += open_to_close[unclosed_brace]

    return closed_json


# jsonの部分文字列を受け取って、parseする。
# Mapのキーの途中で終了している場合は、Noneを返す
def force_parse_json(partial_json, report_error=False, clean_up=True):
    closed_json = close_partial_json(partial_json)
    try:
        response = json.loads(closed_json)
        return clean_up_dict(response) if clean_up else response
    except Exception as e:
        if report_error:
            print(e)
        return None
    
# Remove empty array and empty value from dict
def clean_up_dict(obj):
  if isinstance(obj, dict):
    o = {k: clean_up_dict(v) for k, v in obj.items()}
    o = {k: v for k, v in o.items() if v}
    return o if len(o) > 0 else None
  elif isinstance(obj, list):
    l = [clean_up_dict(v) for v in obj]
    l = [v for v in l if v]
    return l if len(l) > 0 else None
  else:
    return obj