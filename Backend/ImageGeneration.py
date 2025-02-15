import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep
import aiohttp

# function to open and display images based on a given prompt.
def open_images(prompt):
    folder_path = r"Data" # folder where the images are stored.
    prompt = prompt.replace(" ","_") # replace spaces in prompt with underscores.

    # generate the filenames for the images
    Files = [f"{prompt}{i}.jpg" for i in range(1,5)]

    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)

        try:
            # try to open and display the image
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1) # pause for 1 second before showing the next image.

        except IOError:
            print(f"Unable to open {image_path}")

# API details for the Hugging Face Stable Diffusion Model
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

# async function to send a query to the hugging face API
# async def query(payload):
#     response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
#     return response.content


async def query(payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, headers=headers, json=payload) as response:
            return await response.read()

# async function to generate images based on the given prompt
async def generate_images(prompt: str):
    tasks = []

    # create 4 image generation tasks
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed = {randint(0,1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    # Wait for all tasks to complete.
    image_bytes_list = await asyncio.gather(*tasks)

    # Save the generated images to files
    for i, image_bytes in enumerate(image_bytes_list):
        with open(fr"Data\{prompt.replace(' ','_')}{i + 1}.jpg", "wb") as f:
            f.write(image_bytes)

# wrapper function to generate and open images
def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt)) # run the async image generation
    open_images(prompt) # open the generated images.

# main loop to monitor for image generation requests
# while True:

#     try:
#         # read the status and prompt from the data file
#         with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
#             Data: str = f.read()

#         Prompt, Status = Data.split(",")

#         # if the status indicates an image generation request
#         if Status == "True":
#             print("Generating Images...")
#             ImageStatus = GenerateImages(prompt=Prompt)

#             # reset the status in the file after generating images.
#             with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
#                 f.write("False,False")
#                 break # exit the loop after processing the request.

#         else:
#             # await asyncio.sleep(1)
#              sleep(1) # wait for 1 second before checking again

#     # except :
#     #     pass
#     except Exception as e:
#         print(f"Error occurred: {e}")


# this below one is working <3
while True:
    try:
        with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
            Data = f.read().strip()  # Read and strip any extra spaces

        if ',' not in Data:
            print(f"Invalid data format in file: {Data}")
            sleep(1)  # Wait for 1 second before trying again
            continue  # Skip to the next loop iteration

        Prompt, Status = Data.split(",")
        
        # Check if the status is True, meaning image generation request
        if Status == "True":
            print(f"Generating images for prompt: {Prompt}")
            ImageStatus = GenerateImages(prompt=Prompt)
            # Reset status in the file after generating images
            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False,False")
            break  # Exit the loop after processing
        else:
            print(f"Waiting for request... Current status: {Status}")
            sleep(1)

    except Exception as e:
        print(f"Error occurred: {e}")
        break  # Exit loop on error

