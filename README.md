# uticker
An information scroller Twitter trends, news, weather for raspberry pi and **Pimoroni Unicorn Hat Mini** and **Scroll Phat HD**.

## Features include:
* Twitter trends for multiple locations  
* Weather information with many options to display
* News Headlines with configurable items
* Bitcoin prices against other currencies 
* Multithreaded configurable content fetching for smooth scrolling
* Day/Night time brightness for better visibility
* Configurable scroll speed
* Color configuration per scrolling content (unicorn hat only)


## Required Parts:
* Raspberry Pi of any kind
* Pimoroni Unicorn Hat Mini or Scroll Phat HD 
 

## Installation and Running
Install the [Unicorn Hat Mini](https://shop.pimoroni.com/products/unicorn-hat-mini) or [Scroll Phat Hd](https://shop.pimoroni.com/products/scroll-phat-hd?variant=2380803768330) to your raspberry pi and install required libraries. 

Login to your raspberry pi. 

1. Use git to clone the repo.

```bash
git clone https://github.com/tsenyurt/uticker.git
```

2. Change to project folder.

```bash
cd uticker
```

3. Install dependencies.

```bash
pip3 install -r requirements.txt
```

5. Create your own configuration

```bash
mv config.py.sample config.py
```
---
**NOTE**

The configuration file requires API keys and tokens for authentication. The links for API services registration are provided in the config file. 

--- 

4. 
For Unicorn hat mini
```bash
python3 ./uticker.py
```

For scroll phat hd
```bash
python3 ./sticker.py
```

__Happy scrolling!__

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[APACHE](https://www.apache.org/licenses/LICENSE-2.0)