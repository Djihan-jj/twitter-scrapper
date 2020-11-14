from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime


def fetch_tweets(keyword, near, start_date, end_date, scroll_pause_time=1, save=False):
    tweets = []
    num_scrolls = 0
    num_tweets = 0
    try:
        # Prepare for webdriver
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        op.add_argument('window-size=1920x1080')

        # Use webdriver Chrome
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)
        print(f'Scraping tweets for {keyword} from {start_date} to {end_date}')
        
        # Set url
        url = f'https://twitter.com/search?q={keyword}%20until%3A{end_date}%20since%3A{start_date}%20near%3A%22{near}%22%20lang%3Aid&src=typed_query&f=live'
        
        # Hit the URL with driver.get
        print(f">>> URL: {url}")
        driver.get(url)
        
        time.sleep(scroll_pause_time)
        if save:
            f = open(f"data/raw/{keyword}-from-{start_date}-to-{end_date}-DATE_CREATED-{datetime.datetime.now().strftime('%Y-%m-%d-%H.%M.%S')}.csv","w+", encoding="utf-8")

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        tweets = []
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(scroll_pause_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            num_scrolls += 1

            last_tweet = None

            for t in driver.find_elements_by_css_selector('div[data-testid="tweet"]'):
                text = t.find_elements_by_css_selector('div[class="css-1dbjc4n"]')
                num_tweets = num_tweets + 1

                if (len(text) > 2):
                    text = text[2].text.replace("\n", " ")
                    if last_tweet != text:
                        f.writelines(f"{text}\n")

                    last_tweet = text

                print(text)
                tweets.append(text)
                print(f"------> {num_tweets}")

            if new_height == last_height:
                break
            last_height = new_height

        f.close()

        print(f">>> Jumlah tweet diambil : {num_tweets}")
        print(f">>> Jumlah scroll diambil : {num_scrolls}")
    
    except Exception as e:
        print(f">>> Jumlah tweet diambil : {num_tweets}")
        print(f">>> Jumlah scroll diambil : {num_scrolls}")
        print(e)



if __name__ == '__main__':
    input_file = open("input.txt", "r")
    lines = input_file.readlines()

    for line in lines:
        line = line.split(';')
        print(line)
        tweets = fetch_tweets(line[0], line[1], line[2], line[3], scroll_pause_time=5, save=True)
        time.sleep(20)