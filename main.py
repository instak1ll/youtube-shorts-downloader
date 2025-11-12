import tkinter as tk
from tkinter import ttk, filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import yt_dlp
import os
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class YouTubeShortDownloader:
    def __init__(self, master):
        self.master = master
        master.title("YouTube Shorts Downloader")
        master.geometry("600x400")

        self.channel_url = tk.StringVar()
        self.output_path = tk.StringVar()
        self.status = tk.StringVar()
        self.progress = tk.DoubleVar()
        self.downloaded_count = 0
        self.total_links = 0

        ttk.Label(master, text="Channel URL:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(master, textvariable=self.channel_url, width=50).grid(row=0, column=1, columnspan=2, padx=5, pady=5)

        ttk.Label(master, text="Output Folder:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(master, textvariable=self.output_path, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(master, text="Browse", command=self.browse_output_path).grid(row=1, column=2, padx=5, pady=5)

        ttk.Button(master, text="Download Shorts", command=self.start_download).grid(row=2, column=0, columnspan=3, pady=10)

        self.progress_bar = ttk.Progressbar(master, variable=self.progress, maximum=100)
        self.progress_bar.grid(row=3, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

        ttk.Label(master, textvariable=self.status).grid(row=4, column=0, columnspan=3, sticky="w", padx=5, pady=5)

    def browse_output_path(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.output_path.set(folder_selected)

    def start_download(self):
        channel_url = self.channel_url.get()
        output_path = self.output_path.get()

        if not channel_url or not output_path:
            self.status.set("Please enter the channel URL and select an output folder.")
            return

        self.status.set("Starting...")
        Thread(target=self.process_shorts, args=(channel_url, output_path), daemon=True).start()

    def get_short_links(self, channel_url):
        self.status.set("Collecting short links...")
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)

        try:
            driver.get(channel_url)
        except Exception as ex:
            logging.error(f"Error opening channel URL: {ex}")
            driver.quit()
            return []

        try:
            possible_texts = ["Aceptar todo", "Aceptar", "AGREE", "I agree"]
            for txt in possible_texts:
                try:
                    btn = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH,
                            f"//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{txt.lower()}')]"
                        ))
                    )
                    btn.click()
                    logging.debug(f"Clicked cookie button: {txt}")
                    break
                except Exception:
                    continue
        except Exception:
            logging.info("Cookie dialog not found.")

        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        scroll_attempt = 0
        while True:
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                scroll_attempt += 1
                if scroll_attempt >= 3:
                    break
            else:
                scroll_attempt = 0
            last_height = new_height

        links_set = set()
        try:
            elems = driver.find_elements(By.CSS_SELECTOR, "a[href*='/shorts/'], a[href*='watch?v=']")
            for e in elems:
                href = e.get_attribute("href")
                if not href:
                    continue
                if href.startswith("/"):
                    href = "https://www.youtube.com" + href
                if "/shorts/" in href:
                    clean = href.split('?')[0]
                    links_set.add(clean)
                elif "watch?v=" in href:
                    clean = href.split('&')[0]
                    links_set.add(clean)
        except Exception as ex:
            logging.error(f"Error extracting links: {ex}")

        driver.quit()

        self.status.set(f"Found {len(links_set)} shorts.")
        logging.debug(f"Found short links: {links_set}")
        return list(links_set)

    def download_single_short(self, link, index, output_path):
        try:
            ydl_opts = {
                'outtmpl': os.path.join(output_path, f'%(title)s__{index:03d}.%(ext)s'),
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'noplaylist': True,
                'quiet': False,
                'no_warnings': False,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])

            logging.info(f"Short downloaded successfully: {link}")
            return True
        except Exception as e:
            logging.error(f"Error downloading video {index}: {str(e)}")
            return False

    def process_shorts(self, channel_url, output_path):
        short_links = self.get_short_links(channel_url)
        if not short_links:
            self.status.set("No shorts found to download.")
            return

        self.total_links = len(short_links)
        self.downloaded_count = 0
        max_workers = self.total_links 

        self.status.set(f"Starting downloads with {max_workers} concurrent threads...")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for index, link in enumerate(short_links, start=1):
                future = executor.submit(self.download_single_short, link, index, output_path)
                futures.append(future)

            for index, future in enumerate(futures, start=1):
                try:
                    result = future.result()
                    if result:
                        self.downloaded_count += 1
                    self.progress.set(int((index / self.total_links) * 100))
                    self.status.set(f"Downloaded {self.downloaded_count}/{self.total_links}")
                except Exception as e:
                    logging.error(f"Task error: {str(e)}")
                    self.status.set(f"Error in download task: {str(e)}")

        self.status.set(f"Download completed. Downloaded {self.downloaded_count}/{self.total_links} videos.")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeShortDownloader(root)
    root.mainloop()