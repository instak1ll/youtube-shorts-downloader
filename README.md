# YouTube Shorts Downloader

This project allows you to download all YouTube Shorts from a specific channel using Selenium and yt-dlp. The graphical interface is built with Tkinter.

## Requirements

Before running the script, make sure you have the following installed:

- **Python 3.7 or higher**
- **Python Dependencies**: You can install the required dependencies using the `requirements.txt` file.

You can install all dependencies by running the following command in your terminal:

```bash
pip install --user -r requirements.txt
```

## WebDriver Installation

For Selenium to work, you'll need to install a WebDriver compatible with your browser. This project uses Chrome, so you'll need ChromeDriver installed and in your system PATH. Make sure the ChromeDriver version matches your Chrome browser version.

## Usage

1. Clone or download this repository to your local machine.
2. Navigate to the project directory in your terminal.
3. Run the script:

```bash
python main.py
```

4. A graphical interface window will open where you can enter the YouTube channel URL and select the destination folder for downloaded videos.
5. Click "Download Shorts" to start the process.

## Features

- Download all shorts from a YouTube channel
- Concurrent downloads for maximum speed
- Simple and intuitive graphical interface
- Automatic numbering to prevent file overwrites
- Progress tracking with visual progress bar

## Demo

Demonstration video on how to use the downloader:

https://github.com/user-attachments/assets/65cb4150-efb6-4a04-9d3c-742a2b93c24f

## Contributions

If you want to contribute to this project, feel free to open an issue or submit a pull request.

## License

This project is under the MIT License - see the [LICENSE](LICENSE) file for more details.