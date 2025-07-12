from llm_helper import llm
from few_shots import FewShotPosts

few_shot = FewShotPosts()

def get_length(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    return "11 to 15 lines"

def get_prompt(topic, length, lang):
    length_str = get_length(length)
    prompt = f'''
            Generate a LinkedIn post using the below information. No preamble.

            1) Topic: {topic}
            2) Length: {length_str}
            3) Language: {lang}
            If Language is Hinglish then it means it is a mix of Hindi and English. 
            '''
    examples = few_shot.get_filtered_posts(length, lang, topic)
    if len(examples) > 0:
        prompt += "4) Use the writing style as per the following examples:"
        for i, example in enumerate(examples):
            post_text = example["text"]
            prompt += f"\nExample: {i}\n{post_text}"

            if i == 2:
                break
    return prompt


def generate_post(length, lang, topic):
    prompt = get_prompt(topic, length, lang)
    response = llm.invoke(prompt)
    return response.content

if __name__ == "__main__":
    done = generate_post('Medium', 'English', 'Leadership')
    print(done)