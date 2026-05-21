# 도서 관리 프로그램
import pandas as pd
from tkinter import *

window = Tk()

window.title("도서 관리 프로그램")
window.geometry("700x500")


class Book:
    count = 0
    books = []

    @classmethod
    def print_books(cls): # 도서목록 프린트
        print("\n===== 도서 목록 =====")
        print("{:<25} {:<15} {:>8}".format("제목", "저자", "가격"))

        for book in cls.books:
            print(book)

        print(f"\n총 도서 수 : {cls.count}")
        print("=====================\n")

    def __init__(self, title, author, price): #
        self.title = title
        self.author = author
        self.price = price

        Book.count += 1
        Book.books.append(self)

    # 할인 적용
    def discount(self):
        if self.price >= 30000:
            return round(self.price * 0.8)   # 20% 할인

        elif self.price >= 20000:
            return round(self.price * 0.9)   # 10% 할인

        return self.price

    # 객체 출력 형식
    def __str__(self):
        return "{:<25} {:<15} {:>8}원".format(
        self.title,
        self.author,
        self.discount()
    )



# 엑셀 파일 읽기
df = pd.read_excel('book_list.xlsx')
df.columns = df.columns.str.strip()

for i, row in df.iterrows():
    title = row['제목']
    author = row['저자']
    price = row['가격']

    Book(title, author, price)

# 엑셀에 저장하는 함수
def save_books():

    data = []

    for book in Book.books:
        data.append({
            '제목': book.title,
            '저자': book.author,
            '가격': book.price
        })

    df = pd.DataFrame(data)

    df.to_excel('book_list.xlsx', index=False)


def book_ps():
    title = input("제목입력: ").strip()
    author = input("저자입력: ").strip()
    price = input("가격입력: ").strip()
    Book(title,author,int(price))
    save_books()
    print("저장 완료\n")

def book_gum():
    search = input("검색기록: ").strip()

    found = False

    for book in Book.books:

        if search.lower() in book.title.lower():
            print(book)
            found = True

    if found == False:
        print("검색결과 없음\n")

def book_remove():
    search = input("검색기록: ").split()

    found = False

    for book in Book.books:

        if search.lower() in book.title.lower():
            print(book)
            found = True

            remo = input('정말 삭제하시겠습니까?: Y/N ').upper()

            if remo == 'Y':
                Book.books.remove(book)
                Book.count -= 1
                save_books()
                print("삭제 완료\n")

            else:
                print("삭제 취소\n")

            break

    if found == False:
        print("검색결과 없음\n")




while True:
    print("\n0. 책 삭제 \n1. 책추가\n2. 책 목록 출력\n3. 책 검색\n4. 종료\n")

    try:
        int_put = int(input("\n무엇을 도와드릴까요?\n")) 
        print()
        if int_put == 0:
            book_remove()
        elif int_put == 1:
            book_ps()
        elif int_put == 2:
            Book.print_books()
        elif int_put ==3:
            book_gum()
        elif int_put == 4:
            print('종료')
            break
        else:
            print('잘못된 입력입니다.')
            print()
            continue
    except ValueError:
        print("숫자를 입력해주세요")
    except:
        price("프로그램 오류")

window.mainloop()
# 전체 출력
