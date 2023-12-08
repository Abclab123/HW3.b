import pymongo


# Each book has its corresponding collection
# The format of documents in collections is as follows:
# {
#   page : page number,
#   content : text content of this page,
#   pic_id : index of the picture corresponding to the story in this page,
# }
class BooksDB:
    def __init__(self, db_uri: str):
        self.__client = pymongo.MongoClient(db_uri)
        self.__books_db = self.__client.books_db
        self.__books = {}

    def create_book(self, bookname: str):
        if bookname in self.__books_db.list_collection_names():
            raise RuntimeError(f'The book "{bookname}" already existed.')
        self.__books[bookname] = 0

    def append(self, bookname: str, pic_id: int, content: str):
        if self.__books.get(bookname) is None:
            raise RuntimeError(f'The book "{bookname}" is not created yet.')
        self.__books_db[bookname].insert_one(
            {
                "page": self.__books[bookname],
                "content": content,
                "pic_id": pic_id,
            }
        )

        self.__books[bookname] += 1

    def get_book_content(self, bookname: str):
        # return a list of dictionaries
        # [
        #   {
        #     page : page_number,
        #     content:"page 0 text",
        #     pic_id: page 0 picture id(int),
        #   },
        #   {
        #     page : page_number,
        #     content:"page 1 text",
        #     pic_id: page 1 picture id(int),
        #   },
        #   {
        #     page : page_number,
        #     content:"page 2 text",
        #     pic_id: page 2 picture id(int),
        #   },
        #   ...
        # ]

        pages = []
        for page in self.__books_db[bookname].find({}).sort("page", pymongo.ASCENDING):
            pages.append(
                {
                    "page": page["page"],
                    "content": page["content"],
                    "pic_id": page["pic_id"],
                }
            )

        return pages
