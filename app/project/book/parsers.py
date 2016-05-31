from project.utils.parsers import (
    Parser, ModelByIdArgument, MaxLengthArgument, Argument
)

from project.db import Category, Author, User


class BookParser(Parser):

    arguments = (
        MaxLengthArgument(17, 'isbn', required=True,
                          help='ISBN is required'),
        MaxLengthArgument(1024, 'title', required=True,
                          help='Title is required'),
        ModelByIdArgument(Category, 'category', type=int, required=True,
                          help='Category is required'),
        ModelByIdArgument(Author, 'author', type=int, required=True,
                          help='Author is required'),
    )


class LoanParser(Parser):

    arguments = (
        ModelByIdArgument(User, 'user', type=int, required=True,
                          help='Category is required'),
    )
