# 도서 관리 프로그램 GUI 버전
import pandas as pd
from tkinter import *
from tkinter import messagebox
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))

excel_path = os.path.join(BASE_DIR, 'book_list.xlsx')

# 파일 없으면 생성
# 파일 없으면 생성
if not os.path.exists(excel_path):

    df = pd.DataFrame(columns=['제목', '저자', '가격'])

    df.to_excel(excel_path, index=False)

# 엑셀 읽기
df = pd.read_excel(excel_path)

df.columns = df.columns.str.strip()


class Book:
    count = 0
    books = []

    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price

        Book.count += 1
        Book.books.append(self)

    # 할인 적용
    def discount(self):
        if self.price >= 30000:
            return round(self.price * 0.8)

        elif self.price >= 20000:
            return round(self.price * 0.9)

        return self.price

    # 출력 형식
    def __str__(self):
        return "{:<20} {:<15} {:>8}원".format(
            self.title,
            self.author,
            self.discount()
        )

# 엑셀 읽기
df = pd.read_excel('book_list.xlsx')
df.columns = df.columns.str.strip()


for i, row in df.iterrows():
    title = row['제목']
    author = row['저자']
    price = row['가격']

    Book(title, author, price)

# 엑셀 저장
def save_books():

    data = []

    for book in Book.books:
        data.append({
            '제목': book.title,
            '저자': book.author,
            '가격': book.price
        })

    df = pd.DataFrame(data)

    df.to_excel(excel_path, index=False)
# 목록 새로고침
def refresh_list():

    listbox.delete(0, END)

    for book in Book.books:
        listbox.insert(END, str(book))

# 책 추가
def book_add():

    title = title_entry.get().strip()
    author = author_entry.get().strip()
    price = price_entry.get().strip()

    # 입력 체크
    if title == "" or author == "" or price == "":
        messagebox.showwarning("경고", "모든 값을 입력하세요.")
        return

    try:
        price = int(price)

    except:
        messagebox.showerror("오류", "가격은 숫자만 입력하세요.")
        return

    # 객체 생성
    Book(title, author, price)

    # 저장
    save_books()

    # 화면 갱신
    refresh_list()

    # 입력창 초기화
    title_entry.delete(0, END)
    author_entry.delete(0, END)
    price_entry.delete(0, END)

    messagebox.showinfo("완료", "책이 추가되었습니다.")
    hide_input()



# 책 삭제
def book_remove():

    selected = listbox.curselection()

    if not selected:
        messagebox.showwarning("경고", "삭제할 책을 선택하세요.")
        return

    index = selected[0]

    result = messagebox.askyesno("삭제 확인", "정말 삭제하시겠습니까?")

    if result:

        del Book.books[index]
        Book.count -= 1

        save_books()

        refresh_list()

        messagebox.showinfo("완료", "삭제되었습니다.")



# 검색 기능
def book_search():

    keyword = search_entry.get().strip().lower()

    listbox.delete(0, END)

    found = False

    for book in Book.books:

        if keyword in book.title.lower():

            listbox.insert(END, str(book))
            found = True

    if not found:
        messagebox.showinfo("검색 결과", "검색 결과가 없습니다.")

def hide_input():

    title_label.place_forget()
    title_entry.place_forget()

    author_label.place_forget()
    author_entry.place_forget()

    price_label.place_forget()
    price_entry.place_forget()

    save_button.place_forget()

def show_input():

    title_label.place(x=30, y=20)
    title_entry.place(x=80, y=20)

    author_label.place(x=30, y=60)
    author_entry.place(x=80, y=60)

    price_label.place(x=30, y=100)
    price_entry.place(x=80, y=100)

    save_button.place(x=400, y=20)

# 전체 목록 보기
def show_all():

    refresh_list()


# GUI 생성
window = Tk()

window.title("도서 관리 프로그램")
window.geometry("700x500")


# 입력 영역
title_label = Label(window, text="제목")
title_label.place(x=30, y=20)

title_entry = Entry(window, width=30)
title_entry.place(x=80, y=20)

author_label = Label(window, text="저자")
author_label.place(x=30, y=60)

author_entry = Entry(window, width=30)
author_entry.place(x=80, y=60)

price_label = Label(window, text="가격")
price_label.place(x=30, y=100)

price_entry = Entry(window, width=30)
price_entry.place(x=80, y=100)

# 버튼 영역
Button(window, text="책 추가", command=show_input).place(x=400, y=20)
save_button = Button( window, text="저장", width=15, command=book_add)

Button(window, text="책 삭제", width=15, command=book_remove).place(x=400, y=60)

Button(window, text="전체 목록", width=15, command=show_all).place(x=400, y=100)


# 검색 영역
search_entry = Entry(window, width=30)
search_entry.place(x=30, y=160)

Button(window, text="검색", width=10, command=book_search).place(x=250, y=155)



# 리스트 박스
listbox = Listbox(window, width=90, height=15)

listbox.place(x=30, y=220)
hide_input()


# 처음 실행 시 목록 출력
refresh_list()


window.mainloop()