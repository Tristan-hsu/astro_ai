import argparse
import os
import openai
from typing import Callable, List, Dict

from langchain.prompts import PromptTemplate




template = (
    "You are a senior astrologer. "
    "Analyze the meaning of {planet} at {sign} {degree}\u00b0, with speed {speed} and retrogarde state {retrograde}"
)
prompt = PromptTemplate.from_template(template)


def _openai_generator(model_id: str, max_new_tokens: int, temperature: float,api_key: str = None) -> Callable[[str], str]:
    if api_key:
        client = openai.OpenAI(api_key=api_key)
    else:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def _generate(text: str) -> str:
        response = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": text}],
            temperature=temperature,
            max_tokens=max_new_tokens,
        )
        return response.choices[0].message.content

    return _generate




def get_generator(provider: str, model_id: str, max_new_tokens: int, temperature: float, api_key: str = None) -> Callable[[str], str]:
    if provider == "openai":
        return _openai_generator(model_id, max_new_tokens, temperature,api_key)



def generate_responses(docs: List[Dict], provider: str, model_id: str, api_key: str =None) -> List[str]:
    generator = get_generator(provider, model_id, max_new_tokens=256, temperature=0.5, api_key=api_key)
    docs = docs['bodies']
    
    prompts = [
        prompt.format(
            planet=doc["planet"],
            sign=doc["sign"],
            degree=round(doc["sign_degree"], 2),
            speed = doc["speed"],
            retrograde = doc["retrograde"]
        )
        for doc in docs
    ]
    return [generator(text) for text in prompts]

def summurize(inputs:List[str],provider: str, model_id: str, api_key=None) ->str:
    generator = get_generator(provider, model_id, max_new_tokens=10000, temperature=0.5, api_key=api_key)

    summarize_template = ("""You are a senior astrologer. 
    The following is the content:{content},
    Summarize these astrology content into paragraph and description of this person. 
    """)
    prompt_summarize_template = PromptTemplate(template=summarize_template, input_variables=['content'])
    

    translate_template = ("""Your audience is Traditional Chinese Speaker and you are senior translator of Traditional Chinese(繁體中文) and English. 
                          Translate the following content into Traditional Chinese(繁體中文).
                           {english_summary}""")
    
    prompt_translate_template= PromptTemplate(template=translate_template, input_variables=['english_summary'])

    # summurize chain 
    content = "\n".join(inputs)

    summarize_prompt = prompt_summarize_template.format(content=content)
    english_summary = generator(summarize_prompt)

    translate_prompt = prompt_translate_template.format(english_summary=english_summary)
    chinese_summary = generator(translate_prompt)

    return chinese_summary
    


def main() -> None:
    parser = argparse.ArgumentParser(description="LLM provider demo")
    parser.add_argument(
        "--provider",
        choices=["openai"],
        default="openai",
        help="Which backend to use",
    )
    parser.add_argument(
        "--model-id",
        # default="mistralai/Mixtral-8x7B-Instruct-v0.1",
        default='gpt-4o-mini',
        help="Model identifier for the chosen provider",
    )
    args = parser.parse_args()

    docs = {'datetime_utc': '2025-07-03T03:06:00+00:00', 
            'location': {'place': 'Taipei', 
            'latitude': 25.0375198, 'longitude': 121.5636796, 
            'timezone': 'Asia/Taipei'}, 
            'bodies': [
                {'planet': 'Sun', 'degree': 101.4653, 'sign': 'Cancer', 'sign_degree': 11.47, 'speed': 0.953486278600651, 'retrograde': False}, 
                {'planet': 'Moon', 'degree': 194.9444, 'sign': 'Libra', 'sign_degree': 14.94, 'speed': 11.92331047667235, 'retrograde': False}, 
                {'planet': 'Mercury', 'degree': 127.369, 'sign': 'Leo', 'sign_degree': 7.37, 'speed': 1.009335410809777, 'retrograde': False}, 
                {'planet': 'Venus', 'degree': 58.3313, 'sign': 'Taurus', 'sign_degree': 28.33, 'speed': 1.097814049215306, 'retrograde': False}, 
                {'planet': 'Mars', 'degree': 159.0041, 'sign': 'Virgo', 'sign_degree': 9.0, 'speed': 0.5816710326000029, 'retrograde': False}, 
                {'planet': 'Jupiter', 'degree': 95.3009, 'sign': 'Cancer', 'sign_degree': 5.3, 'speed': 0.22742143123066105, 'retrograde': False}, 
                {'planet': 'Saturn', 'degree': 1.8497, 'sign': 'Aries', 'sign_degree': 1.85, 'speed': 0.016802802718145302, 'retrograde': False}, 
                {'planet': 'Uranus', 'degree': 59.8082, 'sign': 'Taurus', 'sign_degree': 29.81, 'speed': 0.04675762032533143, 'retrograde': False},
                {'planet': 'Neptune', 'degree': 2.1746, 'sign': 'Aries', 'sign_degree': 2.17, 'speed': 0.0009440451766443035, 'retrograde': False}, 
                {'planet': 'Pluto', 'degree': 303.0956, 'sign': 'Aquarius', 'sign_degree': 3.1, 'speed': -0.021498338846532548, 'retrograde': True}]
            }
    text_file = open("Output.txt", "a")
    responses = generate_responses(docs,args.provider,args.model_id)
    for output in responses:
        print(output)
        text_file.write(output)

    
    _summurize =summurize(responses,args.provider,args.model_id)
    print(_summurize)
    text_file.write(_summurize)
    text_file.close()

if __name__ == "__main__":
    main()
