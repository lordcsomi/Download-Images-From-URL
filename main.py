import os
import time
import logging
import aiohttp
import asyncio
from PIL import Image
from io import BytesIO


URL = "https://random/url/interesting{}.jpg"
DOWNLOADE_PATH = "images"
TRASHOLD = 2000  # 2KB
START = 0
END = 10000

# stats
starting_time = time.time()
first_index = None
last_index = START -1
success = 0
fail = 0
failed_images = []
not_available = 0

# Calculate the width based on the total number of digits in END
i_width = len(str(END))

async def download_image(session, i):
    global not_available, success, fail, failed_images, first_index, last_index
    url = URL.format(i)
    async with session.get(url) as response:
        if response.status == 200:
            image_content = await response.read()
            if len(image_content) >= TRASHOLD:
                if first_index is None:
                    first_index = i
                if last_index < i:
                    last_index = i

                try:
                    img = Image.open(BytesIO(image_content))
                    img.verify()
                    with open(os.path.join(DOWNLOADE_PATH, f"image_{i:0{i_width}d}.jpg"), "wb") as f:
                        f.write(image_content)
                    success += 1
                    print(f"✅ {i:0{i_width}d}")
                    return "success"
                except Exception as e:
                    fail += 1
                    failed_images.append(i)
                    logging.warning(f"Image_{i}.jpg is not valid, {e}")
                    print(f"⚠️  {i:0{i_width}d}")
                    return "fail"
            else:
                not_available += 1
                print(f"❌ {i:0{i_width}d}")
                return "too_small"
        else:
            not_available += 1
            print(f"❌ {i:0{i_width}d}")
            return "not_available"

async def main():
    global success, fail, failed_images, not_available, first_index, last_index
    if not os.path.exists(DOWNLOADE_PATH):
        os.makedirs(DOWNLOADE_PATH)

    async with aiohttp.ClientSession() as session:
        for i in range(START, END + 1):
            await download_image(session, i)
            
    failed_images = list(set(failed_images))
    while len(failed_images) > 0:
        print ("-" * 20 + "RETRY" + "-" * 20)
        print("Retrying failed images...")
        print(f"Total failed images: {fail}")
        logging.info("-" * 20 + "RETRY" + "-" * 20)
        logging.info(f"Total failed images: {fail}")
        logging.info(f"Failed images: {failed_images}")
        async with aiohttp.ClientSession() as session:
            for i in failed_images:
                result = await download_image(session, i)
                if result == "fail":
                    continue
                elif result == "success":
                    failed_images.remove(i)
                    fail -= 1
                else:
                    print(result)
            
    print ("-" * 20 + "STATS" + "-" * 20)
    print("Download complete.")
    print(f"Total time taken: {time.time() - starting_time}")
    print(f"checked a total of {success + fail + not_available} images")
    print(f"success: {success}, fail: {fail}, not_available: {not_available}")
    print(f"total downloadables: {success + fail}")
    print(f"download success rate: {round((success / (success + fail) * 100), 2)}%")
    print(f"first download: {first_index}")
    print(f"last download: {last_index}")
    
    logging.info("-" * 20 + "STATS" + "-" * 20)
    logging.info(f"Total time taken: {time.time() - starting_time}")
    logging.info(f"checked a total of {success + fail + not_available} images")
    logging.info(f"success: {success}, fail: {fail}, not_available: {not_available}")
    logging.info(f"total downloadables: {success + fail}")
    logging.info(f"download success rate: {round((success / (success + fail) * 100), 2)}%")
    logging.info(f"first download: {first_index}")
    logging.info(f"last download: {last_index}")

if __name__ == "__main__":
    logging.basicConfig(filename='app.log', filemode="w", level=logging.INFO, format='%(asctime)s - %(message)s', encoding='utf-8')
    logging.info(f"Starting the download process at {time.strftime('%H:%M:%S', time.localtime())}")
    logging.info(f"START: {START}, END: {END}")
    asyncio.run(main())
