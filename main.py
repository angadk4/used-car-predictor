import scraper
import createmodel
import time

SCROLL_RANGE = 3
def main():
    sc = scraper.Scraper()
    sc.load_url()
    print("Loaded KJIJI AUTOS...")
    for i in range(SCROLL_RANGE):
        time.sleep(2)
        sc.scroll_down()
        print("Scroll " + str(i+1))
    print("Done scrolling, waiting for load...")
    time.sleep(5)
    print("Reading data now...")
    sc.read_data()
    print(sc.get_hrefs())
    print(sc.get_features("https://www.kijijiautos.ca/" + str(sc.hrefs[0])))
    print("\n\nFinished Running Script")
    time.sleep(300)

if __name__ == "__main__":
    main()
