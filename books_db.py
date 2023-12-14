## 9
# In this module, you need to use mongoDB to create a database for books.
# Each book has its corresponding table.
# The format of the elements of the collections are : {page : page_number, content : the text content of this page, picture_idx : the index of the picture corresponding to the story in this page.}
# MongoDB
import pymongo


class BooksDB:
    def __init__(self, myclient: str):
        self.myclient = pymongo.MongoClient(myclient)
        self.mydb = self.myclient["mydatabase"]

    def create_book(self, bookname: str):
        # 創建新書籍，如果不存在的話
        if bookname not in self.mydb.list_collection_names():
            self.mydb[bookname].insert_one(
                {"page": 1, "content": "", "picture_idx": None}
            )
            print("Book created successfully")
        else:
            print("Book already exists")

    def append(self, bookname: str, picture_idx: int, content: str):
        # 在指定書籍中追加新頁面的數據
        collection = self.mydb[bookname]
        last_page = collection.find_one(sort=[("page", pymongo.DESCENDING)])
        new_page_number = last_page["page"] + 1
        collection.insert_one(
            {"page": new_page_number, "content": content, "picture_idx": picture_idx}
        )
        print("Page added successfully")


if __name__ == "__main__":
    # 創建 BooksDB 實例
    my_books_db = BooksDB("mongodb://localhost:27017/")

    # 創建一本名為 "MyBook" 的書籍
    my_books_db.create_book("MyBook")

    # 向 "MyBook" 書籍中的第一頁添加內容和圖片索引
    my_books_db.append("MyBook", picture_idx=1, content="這是第一頁的內容。")

    print(my_books_db.mydb.list_collection_names())
