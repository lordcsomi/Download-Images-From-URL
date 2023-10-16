import os
import aiohttp
import asyncio
from PIL import Image
from io import BytesIO

# URL template
base_url = "https://kisnaplo.karinthy.hu/app/interface.php?view=v_download_photo&target=PLWS{}.jpg&type=order&KSNPLSID=ndmqcnsi0uass2cqk1qt6vgv47&KSNPLSID=ndmqcnsi0uass2cqk1qt6vgv47"
DOWNLOADE_PATH = "images"

async def download_image(session, i):
    url = base_url.format(i)
    async with session.get(url) as response:
        if response.status == 200:
            image_content = await response.read()
            if len(image_content) >= 2000:
                # Validate the image using Pillow (PIL)
                try:
                    img = Image.open(BytesIO(image_content))
                    img.verify()  # This will raise an error if the image is corrupt
                    with open(os.path.join(DOWNLOADE_PATH, f"image_{i}.jpg"), "wb") as f:
                        f.write(image_content)
                    print(f"Downloaded image_{i}.jpg")
                except Exception as e:
                    print(f"Image_{i}.jpg is downloaded")
            else:
                print(f"Image_{i}.jpg is not available")
        else:
            print(f"Failed to download image_{i}.jpg")

async def main():
    # chechk if the download folder exists
    if not os.path.exists(DOWNLOADE_PATH):
        os.makedirs(DOWNLOADE_PATH)
    
    async with aiohttp.ClientSession() as session:
        # Loop through numbers 0-5000
        for i in range(5001):
            await download_image(session, i)

    print("Download complete.")

if __name__ == "__main__":
    asyncio.run(main())
