from langchain_classic.chains.constitutional_ai.prompts import examples
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_community.llms.tongyi import Tongyi
example_template=PromptTemplate.from_template("单词：{word},反义词：{antonym}")

#示例的动态数据注入
examples_data=[
    {"word":"大","antonym":"小"},
    {"word":"上","antonym":"下"}
]
few_shot_template=FewShotPromptTemplate(
    example_prompt=example_template,
    examples=examples_data,
    prefix="告知我单词的反义词，我提供如下的示例：",
    suffix="基于前面的示例告知我，{input_word}的反义词是？",
    input_variables=['input_word'],
)

prompt_text=few_shot_template.invoke(input={"input_word":"左"}).to_string()
print(prompt_text)

model=Tongyi(model="qwen-max")
print(model.invoke(input=prompt_text))