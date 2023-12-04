from openai import OpenAI

class OpenAIGenerator:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.system_prompt = "We are going to play a game called Story Chain. "\
            "The user starts by telling the beginning of a story, and then you "\
            "and the user take turns continuing the story until it reaches a "\
            "suitable conclusion."

    def generate(self, user_input: str, history: list = []) -> str:
        messages = [{"role": "system", "content": self.system_prompt}]
        for i, message in enumerate(history):
            if i % 2 == 0:
                messages.append({"role": "user", "content": message})
            else:
                messages.append({"role": "assistant", "content": message})
        messages.append({"role": "user", "content": user_input})

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages
        )
        return response.choices[0].message.content

if __name__ == "__main__":
    import configparser
    config = configparser.ConfigParser()
    config.read('config.ini')
    openai_generator = OpenAIGenerator(config["OpenAI"]["api_key"])

    # test without history
    print("Test without history.")
    user_input = "從前從前，有一個小男孩，名字叫小智。"
    output = openai_generator.generate(user_input)
    print(output)
    print("="*100)
    
    # test with history
    print("Test with history.")
    history = [
        "從前從前，有一個小男孩，名字叫小智。",
        "小智是一個非常好奇、勇敢的小男孩。他住在一個小村莊裡，村莊周圍是茂密的森林和高聳的山脈。"\
        "小智非常喜歡探險，他經常和他的好朋友小狗小黑一起在村莊和森林裡遊玩。有一天，小智決定要到"\
        "村莊外的神秘森林裡去探險，因為他聽說那裡有很多神奇的生物和寶藏。",
    ]
    user_input = "在出發前，小智的爺爺提醒他，神秘森林雖然有許多有趣的事物，但探險的過程也有可能遇到無法預期的危險。"
    output = openai_generator.generate(user_input, history)
    print(output)