This is a sample that could self-prompt GPT itself without re.
Also, this could enable the GPT could keep their memory.


1st trial:
XXX % python3 Automatic\ prompt_framework.py

🔍 **check 1th data**
prompting_word_from_first_GPT_Agent Prompt for GPT-3:

Given the following text, please extract the tasks mentioned and organize them into a structured format. The format should include three columns: 'Task Name', 'Time', and 'Notes'. If there are any specific notes related to a task, please include them in the 'Notes' column. Here is the text:

"Mop the floor 8 AM, clean the kitchen 1 PM, feed my cats 3 PM (MiGu could eat less since she's fat) and walk my dog 5PM"
reply_from_second_GPT_Agent | Task Name       | Time | Notes                             |
|-----------------|------|-----------------------------------|
| Mop the floor   | 8 AM |                                   |
| Clean the kitchen | 1 PM |                                   |
| Feed my cats    | 3 PM | MiGu could eat less since she's fat |
| Walk my dog     | 5 PM |                                   |
👉 **Do you think this is okay？** (y: correct, n: Error, q: Quit Checking) y
📁 Revised results have been stored self_prompt.csv
 
