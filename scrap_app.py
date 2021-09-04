from tkinter import *
import bs4
import requests
import os

root = Tk()

root.title("Snapdeal Images Search")
# Set geometry(widthxheight)
root.geometry('500x350')


lbl = Label(root, text = "Enter Your Query")
lbl.grid()
lbl2 = Label(root, text = "")
lbl2.grid()
lbl3 = Label(root, text = "")
lbl3.grid()



txt = Entry(root, width=10)
txt.grid(column =1, row =0)


def clicked():

    str = txt.get()
    input_str = str
    str = str.replace(" ", "&20")


    url = "https://www.snapdeal.com/search?keyword={}&santizedKeyword=&catId=&categoryId=0&suggested=false&vertical=&noOfResults=20&searchState=&clickSrc=go_header&lastKeyword=&prodCatId=&changeBackToAll=false&foundInAll=false&categoryIdSearched=&cityPageUrl=&categoryUrl=&url=&utmContent=&dealDetail=&sort=rlvncy".format(str)
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content)
    picture_element = soup.findAll('picture')
    count = 0
    try: 
        os.mkdir(input_str)
        for i, picture in enumerate(picture_element):
            count = i
            with open('{}/{}-{}.jpg'.format(input_str, input_str, i), 'wb') as file:
                try:
                    img_url = picture.img.attrs['src']
                    response = requests.get(img_url)
                    file.write(response.content)
                except KeyError:
                    img_url = picture.img.attrs['data-src']
                    response = requests.get(img_url)
                    file.write(response.content)
    except FileExistsError:
        text = "The search keyword is same to a previously searched keyword. Therefore, deleting old files."
        lbl2.configure(text = text)
        for f in os.listdir(input_str):
            os.remove(os.path.join(input_str, f))
        for i, picture in enumerate(picture_element):
            count = i
            with open('{}/{}-{}.jpg'.format(input_str, input_str, i), 'wb') as file:
                try:
                    img_url = picture.img.attrs['src']
                    response = requests.get(img_url)
                    file.write(response.content)
                except KeyError:
                    img_url = picture.img.attrs['data-src']
                    response = requests.get(img_url)
                    file.write(response.content)

    text = "{} new files are saved in the newly created folder".format(count)
    lbl2.configure(text = text)

search_btn = Button(root, text = "Search" ,
            fg = "black", command=clicked)


search_btn.grid(column=2, row=0)

root.mainloop()
