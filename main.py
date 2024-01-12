import scraper
import createmodel
import time

SCROLL_RANGE = 100
def main():
    sc = scraper.Scraper()
    sc.load_url()
    print("Loaded KJIJI AUTOS...")
    for i in range(SCROLL_RANGE):
        time.sleep(4)
        sc.scroll_down()
        print("Scroll " + str(i+1))
    print("Done scrolling, waiting for load...")
    time.sleep(120)
    print("Reading data now...")
    sc.read_data()
    print(sc.get_hrefs())
    for h in sc.get_hrefs():
        print(h)
        data = sc.get_info("https://www.kijijiautos.ca/" + str(h))
        sc.csv_manage(data)
        #print(data)
    print("\n\nFinished Running Script")
    time.sleep(12000)

if __name__ == "__main__":
    main()
