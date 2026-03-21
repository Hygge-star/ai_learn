"""
json.dumos(字典或列表，ensure_ascii=False

json.loads(json字符串)：将json字符串转换为Python
返回值：Oython字典或Python列表
"""

import json
d={
    "name":"小明",
    "age":18,
    "gender":"male"
}

s=json.dumps(d,ensure_ascii=False)
print(s)

l=[
    {
        "name":"xiaoming",
        "age":18,
        "gender":"male"
    },
    {
        "name":"xiao",
        "age":18,
        "gender":"male"
    },
    {
        "name":"xiao",
        "age":18,
        "gender":"male"

    }
]

print(json.dumps(l,ensure_ascii=False))

json_str = '{"name":"xiao","age":18,"gender":"male"}'
json_array_str='{"name":"xiao","age":18,"gender":"male"},{"name":"xiao","age":18,"gender":"female"}'
res_dict=json.loads(json_str)
print(res_dict,type(res_dict))