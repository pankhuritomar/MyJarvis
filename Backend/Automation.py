# THIS ONE'S FOR TASK EXECUTION

# line 232, the star thing.


from AppOpener import close, open as appopen # import functions to open and close apps.
from webbrowser import open as webopen # import web browser functionality.
from pywhatkit import search, playonyt # import functions for google search and playback.
from dotenv import dotenv_values # import dotenv to manage environment variables.
from bs4 import BeautifulSoup # import BeautifulSoup for parsing HTML content.
from rich import print # import rich for styled console output.
from groq import Groq # import Groq for AI chat functionalities.
import webbrowser # for opening URLs
import subprocess # for interacting with the system.
import requests # for making HTTP requests.
import keyboard # for keyboard-related actions.
import asyncio # for asynchronous programming
import os # for operating system functionalities.

# load environment variables from the.env file.
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey") # retrieve the Groq API key.

# define CSS classes for parsing specific elements in HTML content.
classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "O5uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaOe", "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

# define a user-agent for making web requests.
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# initialize the Groq client with the API key.
client = Groq(api_key=GroqAPIKey)

# predefined professional responses for user interactions.
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need-don't hesitate to ask.",
]
 
# list to store chatbot messages.
messages = []

# System message to provide context to the chatbot.
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poem, etc. "}]

# function to perform a google search
def GoogleSearch(Topic):
    search(Topic) # use pywhatkit's search function to perform a google search.
    return True # indicates success.

# function to generate content using AI and save it to a file.
def Content(Topic):

    # nested function to open a file in Notepad.
    def OpenNotepad(File):
        default_text_editor = 'notepad.exe' # default text editor.
        subprocess.Popen([default_text_editor, File]) # open the file in Notepad.

    # nested function to generate content using the AI chatbot.
    def ContentWriterAI(prompt):
        messages.append({"role":"user", "content": f"{prompt}"}) # add the user's prompt to messages.

        completion = client.chat.completions.create (
            model= "mixtral-8x7B-32768", # specify the AI model.
            messages= SystemChatBot + messages, # include system instructions and chat history
            max_tokens=2048, # limit the maximum tokens in the response
            temperature=0.7, # adjust response randomness
            top_p=1, # enable streaming response
            stream=True, # enable streaming response
            stop=None # allow the model to determine stopping conditions
        )
            
        

        Answer = "" # initialize an empty string for the response.

        # process streamed response chunks.
        for chunk in completion:
            if chunk.choices[0].delta.content: # check for content in the current chunk.
                Answer += chunk.choices[0].delta.content  # append the content to the answer.

        Answer = Answer.replace("</s>", "") # remove unwanted tokens from the response.
        messages.append({"role": "assistant", "content":Answer}) # add the AI's response to messages.
        return Answer
    
    Topic: str = Topic.replace("Content", "") # remove "content " from the topic
    ContentByAI = ContentWriterAI(Topic) # generate content using AI.

    # Save the generated content to a text file
    with open(rf"Data\{Topic.lower().replace(' ','')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI) # write the content to the file.
        file.close()

    OpenNotepad(rf"Data\{Topic.lower().replace(' ','')}.txt") # open the file in Notepad
    return True # indicate success.

# Content("application for a sick leave.")
# function to search for a topic on youtube.
def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}" # construct the youtube search URL.
    webbrowser.open(Url4Search) # open the search URL in a web browser.
    return True  # indicates success.

# YouTubeSearch("code with harry")
def PlayYoutube(query):
    playonyt(query) # use pywhatkit's function to play the video.
    return True # indicates success

# function to open an apllication or a relevant webpage.
def OpenApp(app, sess=requests.session()):

    try:
        appopen(app, match_closest=True, output=True, throw_error=True) # attempt to open the app.
        return True # indicate success.
    
    except: 
        # nested function to extract links from the HTML content.
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser') # parse the HTML content.
            links = soup.find_all('a', {'jsname': 'UWckNb'}) # find relevant links.
            return [link.get('href') for link in links] # return the links.
        
        # nested function to perform a Google search and retrieve HTML.
        def search_google(query):
            url = f"https://www.google.com/search?q={query}" # construct the google search URL
            headers = {"User-Agent": useragent} # use the predefined user-agent.
            response = sess.get(url, headers=headers) # performs the GET request.

            if response.status_code == 200:
                return response.text # return the html content.
            else:
                print("Failed to retrieve search results.") # print an error message.
                return None
            
        html = search_google(app) # perform the Google search.

        if html:
            link = extract_links(html)[0] # extract the first link from the search results.
            webopen(link) # open the link in a web browser.

        return True # indicates success
    
# function to close an application
def CloseApp(app):

    if "chrome" in app:
        pass # Skip is the app is Chrome. BECAUSeee humne speech to text wale code me selenium use kara hai, toh wo bhi band hojayega.
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True) # attempt to close the app
            return True # indicates success
        except:
            return False # indicates failure.

CloseApp("settings")      
# function to execute system-level commands.
def System(command):

    # nested function to mute the system volume.
    def mute():
        keyboard.press_and_release("volume mute") # simulate the mute key press.

    # nested function to unmute the system volume.
    def unmute():
        keyboard.press_and_release("volume unmute") # simulate the unmute key press.
    # nested function to unmute the system volume.
    def volume_up():
        keyboard.press_and_release("volume up") # simulate the volume up key press.

    # nested function to decrease the system volume.
    def volume_down():
        keyboard.press_and_release("volume down") # simulate the volume down key press.

    # execute the appropriate command.
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()

    return True # success

# asynchronous function to translate and execute user commands.
async def TranslateAndExecute(commands: list[str]):

    funcs = [] # list to store asynchronous tasks.

    for command in commands:

        if command.startswith("open "): # handle "open" commands.

            if "open it" in command: # ignore "open it" commands.
                pass

            if "open file" == command: # ignore "open file" commands.
                pass

            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open ")) # schedule app opening.
                funcs.append(fun)

        elif command.startswith("general "): # placeholder for general commands.
            pass

        elif command.startswith("realtime "): # placeholder for realtime commands.
            pass

        elif command.startswith("close "): # handle "close " commands.
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close ")) # schedule app closing
            funcs.append(fun)

        elif command.startswith("play "): # handle "play" commands.
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play ")) # schedule YouTube playback.
            funcs.append(fun)

        elif command.startswith("content "): # handle "content" commands.
            fun = asyncio.to_thread(Content, command.removeprefix("content ")) # Schedule content creation.
            funcs.append(fun)

        elif command.startswith("google search "): # handle google search commands.
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search ")) # schedule google search
            funcs.append(fun)

        elif command.startswith("youtube search "): # handle youtube search commands.
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search ")) # schedule youtube search
            funcs.append(fun)

        elif command.startswith("system "): # handle system commands.
            fun = asyncio.to_thread(System, command.removeprefix("system ")) # schedule system search
            funcs.append(fun)
        
        else :
            print(f"No Function Found. For {command}") # print an error for unrecognized commands.

    results = await asyncio.gather(*funcs) # execute all tasks concurrently.

    for result in results: # process the results.
        if isinstance(result,str):
            yield result
        else:
            yield result

# asynchronous function to automate command execution.
async def Automation(commands: list[str]):

    async for result in TranslateAndExecute(commands): # translate and execute commands.
        pass
    return True # indicate success.

if __name__ == "__main__":
    # Pass a list of commands to the Automation function
    asyncio.run(Automation([
        "open facebook", 
        "open instagram", 
        "open telegram", 
        "play iraday"
    ]))






        
         