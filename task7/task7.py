import os
import time
import requests
import asyncio
import aiohttp


os.makedirs("kittens_sync", exist_ok=True)
os.makedirs("kittens_async", exist_ok=True)

URL = "https://loremflickr.com/1280/720/kittens"


# ============== СИНХРОННАЯ ЗАГРУЗКА ==============

def download_one_sync(i):
    """
    Скачивает одно изображение котёнка синхронным способом и сохраняет его на диск.
    
    Аргументы:
        i (int): Порядковый номер изображения (для именования файла).
    """
    print(f"Синхронно: начинаю скачивать kitten {i}")
    response = requests.get(URL)
    with open(f"kittens_sync/kitten_{i}.jpg", "wb") as f:
        f.write(response.content)
    print(f"Синхронно: kitten {i} сохранён")


def run_sync():
    """
    Выполняет последовательную (синхронную) загрузку 5 изображений котят.
    Выводит общее время выполнения.
    """
    print("--- СИНХРОННАЯ ЗАГРУЗКА")
    start = time.time()
    for i in range(1, 6):
        download_one_sync(i)
    end = time.time()
    print(f"Синхронно завершено за {end - start} секунд\n")


# ============== АСИНХРОННАЯ ЗАГРУЗКА ==============

async def download_one_async(i):
    """
    Асинхронно скачивает одно изображение котёнка и сохраняет его на диск.
    
    Аргументы:
        i (int): Порядковый номер изображения (для именования файла).
    """
    print(f"Асинхронно: начинаю скачивать kitten {i}")
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            content = await response.read()
            with open(f"kittens_async/kitten_{i}.jpg", "wb") as f:
                f.write(content)
    print(f"Асинхронно: kitten {i} сохранён")


async def run_async():
    """
    Выполняет асинхронную загрузку 5 изображений котят параллельно.
    Выводит общее время выполнения.
    """
    print("--- АСИНХРОННАЯ ЗАГРУЗКА")
    start = time.time()
    tasks = []

    for i in range(1, 6):
        task = download_one_async(i)
        tasks.append(task)
    
    #await asyncio.gather(tasks[0], tasks[1], tasks[2], tasks[3], tasks[4])
    await asyncio.gather(*tasks)  

    end = time.time()
    print(f"Асинхронно завершено за {end - start} секунд\n")


if __name__ == "__main__":
    run_sync()
    asyncio.run(run_async())