import json
import requests
import pandas as pd

import json
import pandas as pd
import os
import csv

# API Parameters

# Second GPT
def send_to_gpt2(temp=0, original=None, calendar="", conversation=[], previous_prompt = None, Scores = None, user_input = None, plz_correct = False):
    messages = [
        {"role": "system", "content": "You are a prompt engineeer."},
    ]
    if plz_correct == True:
        user_message = f"""
        We are doing the prompting work, but I don't like my existing prompt, 
        reasons: 
            {user_input}
            My input: Mop the floor 8 AM, clean the kitchen 1 PM, feed my cats 3 PM (MiGu could eat less since she's fat) and walk my dog 5PM

            My desired output:
                Task Name,Time,Notes
                Mop the floor, 8 AM,
                clean the kitchen, 1 PM,
                feed my cats, 3PM, MiGu could eat less since she's fat
                walk my dog, 5PM,
            Please do not mention my desired output when prompting, thanks. (zero-shot)
            Please help me generate the prompt again..Thanks
        """
    else:
        user_message = f"""
        Introduction: 
        I'm going to use two GPTs, one is you and you're going to tell another GPT to do following work.
        I need your help to generate a prompt for another GPT based on the original text, generating the Expected output as follow:
        
        Original Text: Mop the floor 8 AM, clean the kitchen 1 PM, feed my cats 3 PM (MiGu could eat less since she's fat) and walk my dog 5PM

        Expected Output for GPT: 
        Task Name,Time,Notes
        Mop the floor, 8 AM,
        clean the kitchen, 1 PM,
        feed my cats, 3PM, MiGu could eat less since she's fat
        walk my dog, 5PM,

        Please do not mention my desired output when prompting, thanks. (zero-shot)

        
        
        """

    messages.append({"role": "user", "content": user_message})

    body = json.dumps({
        "messages": messages,
        "temperature": temp
    })

    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.post(URL, headers=HEADERS, data=body)
            response.raise_for_status()
            gpt_response = json.loads(response.text)['choices'][0]['message']['content']
            

            return gpt_response 
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}, retrying...")
            retries += 1
            # print("conversation",conversation)
    return gpt_response


# First GPT
def send_to_gpt(temp=0, original=None, calendar="", conversation=[], Scores = None, prompting = None):
    
    messages = [
        {"role": "system", "content": ""},
    ]
    
    # **History extension**
    messages.extend(conversation)

    # **New question**

    user_message = f"""
    {prompting}
    """

    messages.append({"role": "user", "content": user_message})

    body = json.dumps({
        "messages": messages,
        "temperature": temp
    })

    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.post(URL, headers=HEADERS, data=body)
            response.raise_for_status()
            gpt_response = json.loads(response.text)['choices'][0]['message']['content']
            
            return gpt_response
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}, retrying...")
            retries += 1
    return gpt_response

# # Read data if you could like the prompting to contain specific context
# df_clean = pd.read_csv('')
data = {"Column1": ["Value1"], "Column2": ["Value2"], "Column3": ["Value3"]}

# 創建 DataFrame
df_clean = pd.DataFrame(data)

results = []

# Stop_flag for debuggin testing
stop_flag = False
conversation = []  # History Conversation

# conversation.append(prompt_2)
accu = 0
promptings = []
promptings_temp = []
for index, row in df_clean.iterrows():
    if stop_flag:
        break  # Break the for loop if the stop flag == 1
    if index>5:
        stop_flag =1
    print(f"🔍 **check {index+1}th data**")

    # Make GPT process

    
    promptings_temp = promptings #temporary storage

    prompting = send_to_gpt2(0 )
    print("prompting_word_from_first_GPT_Agent", prompting)
    promptings_temp.append(prompting)
    result_self_prompt = send_to_gpt(0, prompting = promptings_temp)
    
    print("reply_from_second_GPT_Agent",result_self_prompt)
    while True:
        user_input = input("👉 **Do you think this is okay？** (y: correct, n: Error, q: Quit Checking) ").strip().lower()

        if user_input == "y":
            promptings.append(promptings_temp)
            
            accu += 1
            break
        elif user_input == "n":
            user_input = input("👉 I don't like prompting, reasons").strip().lower()

            prompting = send_to_gpt2(0 , user_input = user_input, previous_prompt = promptings, plz_correct = True)
            print("prompting",prompting)  
            promptings_temp =  promptings #I discharge the previous prompt bc I would like to ignore the undesired prompt to improve accuaracy.
            promptings_temp.append(prompting)
            # Ajusted the GPT input again
            print("\n Prompt the GPT again")
            result_self_prompt = send_to_gpt(0 , prompting = promptings_temp)
            print(f" GPT reply: {prompting}")

            while True:
                confirm_input = input("👉 **Do you think this is okay？** (y: Continue, n: revise, q: Stop Checking) ").strip().lower()
                if confirm_input == "y":
                    promptings.append(prompting)
                    break
                elif confirm_input == "q":
                    stop_flag = True
                    break
                elif confirm_input == "n":
                    break
                else:
                    print(" Please enter 'y', 'n', or 'q'.")
            if stop_flag:
                break
                    
        elif user_input == "q":
            print(" **Stop checking and Store the results...**")
            stop_flag = True
            break
        else:
            print("⚠️ Please type 'y', 'n' or 'q'。")
    
    results.append({"reply from second GPT": promptings})
    
    df = pd.DataFrame(promptings, columns=["prompt"])  # 設定標題
    df.to_csv("prompts.csv", index=False, encoding="utf-8")
    

# Store the result
output_file = "self_prompt.csv"
pd.DataFrame(results).to_csv(output_file, index=False)
print(f"📁 Revised results have been stored {output_file}")
