import tkinter as tk
from tkinter import ttk, filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import yt_dlp
import os
from threading import Thread
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

        ttk.Label(master, text="Canal URL:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(master, textvariable=self.channel_url, width=50).grid(row=0, column=1, columnspan=2, padx=5, pady=5)

        ttk.Label(master, text="Carpeta de destino:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(master, textvariable=self.output_path, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(master, text="Explorar", command=self.browse_output_path).grid(row=1, column=2, padx=5, pady=5)

        ttk.Button(master, text="Descargar Shorts", command=self.start_download).grid(row=2, column=0, columnspan=3, pady=10)

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
            self.status.set("Por favor, ingresa la URL del canal y selecciona una carpeta de destino.")
            return

        self.status.set("Iniciando proceso...")
        Thread(target=self.process_shorts, args=(channel_url, output_path)).start()

    def get_short_links(self, channel_url):
        self.status.set("Obteniendo enlaces de shorts...")
        driver = webdriver.Chrome()
        driver.get(channel_url)
        
        try:
            cookie_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Aceptar todo')]"))
            )
            cookie_button.click()
        except:
            logging.info("No se encontró el botón de cookies o ya estaban aceptadas.")
        
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        shorts_links = soup.find_all('a', class_='ShortsLockupViewModelHostEndpoint')
        
        links = set(f"https://www.youtube.com{link['href']}" for link in shorts_links)
        
        driver.quit()
        
        self.status.set(f"Se encontraron {len(links)} shorts.")
        logging.debug(f"Enlaces de shorts encontrados: {links}")
        return list(links)

    def process_shorts(self, channel_url, output_path):
        short_links = self.get_short_links(channel_url)
        if not short_links:
            self.status.set("No se encontraron shorts para descargar.")
            return

        total_links = len(short_links)
        for index, link in enumerate(short_links, start=1):
            try:
                ydl_opts = {
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'format': 'best[ext=mp4]',
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    self.status.set(f"Descargando short {index}/{total_links}")
                    ydl.download([link])
                
                self.status.set(f"Descargado {index}/{total_links}")
                logging.info(f"Short descargado exitosamente: {link}")
            except Exception as e:
                logging.error(f"Error al descargar video {index}/{total_links}: {str(e)}")
                self.status.set(f"Error al descargar video {index}/{total_links}: {str(e)}")
            finally:
                self.progress.set(int((index / total_links) * 100))

        self.status.set("Descarga completada.")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeShortDownloader(root)
    root.mainloop()