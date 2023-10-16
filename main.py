import aiohttp
import asyncio

# URL template
base_url = ""

async def download_image(session, i):
    url = base_url.format(i)
    async with session.get(url) as response:
        if response.status == 200:
            image_content = await response.read()
            if len(image_content) >= 2000:
                with open(f"image_{i}.jpg", "wb") as f:
                    f.write(image_content)
                print(f"Downloaded image_{i}.jpg")
            else:
                print(f"Image_{i}.jpg is too small")
        else:
            print(f"Failed to download image_{i}.jpg")

async def main():
    async with aiohttp.ClientSession() as session:
        # Load the list of checked images from a file (if it exists)
        checked_images = set()
        try:
            with open("checked_images.txt", "r") as f:
                checked_images = set(int(line.strip()) for line in f)
        except FileNotFoundError:
            pass

        # Loop through numbers 0-5000
        for i in range(10001):
            if i not in checked_images:
                await download_image(session, i)
                checked_images.add(i)

                # Save the checked images to the file
                with open("checked_images.txt", "a") as f:
                    f.write(f"{i}\n")

    print("Download complete.")

if __name__ == "__main__":
    asyncio.run(main())
