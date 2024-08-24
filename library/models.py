from django.contrib.auth.models import User

from django.db import models


def book_directory_path(instance, filename):
    return 'library/books/book_{0}/{1}'.format(instance.pk, filename)


class Book(models.Model):
    img = models.ImageField(upload_to=book_directory_path, null=True, default='library/nobook.jpg',
                            verbose_name="Обложка")
    index = models.CharField(blank=True, max_length=50, verbose_name="Индекс")
    author_mark = models.CharField(blank=True, max_length=50, verbose_name="Авторский знак")
    author = models.CharField(blank=True, max_length=200, verbose_name="Автор")
    title = models.CharField(blank=True, max_length=500, verbose_name="Название")
    pub_place = models.CharField(blank=True, max_length=100, verbose_name="Место издания")
    publishing = models.CharField(blank=True, max_length=200, verbose_name="Издательство")
    pub_date = models.CharField(blank=True, max_length=50, verbose_name="Год издания")
    num_pages = models.CharField(blank=True, max_length=50, verbose_name="Количество страниц")
    invent_number = models.CharField(blank=True, max_length=50, verbose_name="Инвентарный номер")
    price = models.CharField(blank=True, max_length=50, verbose_name="Цена")
    number_of_copies = models.CharField(blank=True, null=True, max_length=50, verbose_name="Количество экземпляров")
    num_in_issue_book = models.CharField(blank=True, max_length=50, verbose_name="Номер в книге выдачи")
    date_create = models.DateTimeField(null=True, auto_now_add=True, verbose_name="Создано")

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return self.title


def article_directory_path(instance, filename):
    return 'library/articles/article_{0}/{1}'.format(instance.pk, filename)


class Article(models.Model):
    index = models.CharField(blank=True, max_length=50, verbose_name="Шифр")
    author_lastname = models.CharField(blank=True, max_length=200, verbose_name="Фамилия автора")
    author_initials = models.CharField(blank=True, max_length=20, verbose_name="Инициалы автора")
    title_article = models.CharField(blank=True, max_length=500, verbose_name="Название статьи")
    title_magazine = models.CharField(blank=True, max_length=500, verbose_name="Название журнала")
    pub_date = models.CharField(blank=True, max_length=50, verbose_name="Год издания")
    pub_number = models.CharField(blank=True, max_length=50, verbose_name="Номер журнала")
    num_pages = models.CharField(blank=True, max_length=50, verbose_name="Количество страниц")
    file = models.FileField(blank=True, null=True, upload_to=article_directory_path,
                            verbose_name="Электронная версия статьи")
    date_create = models.DateTimeField(null=True, auto_now_add=True, verbose_name="Создано")

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return self.title_article


class Reader(models.Model):
    name = models.CharField(max_length=255, verbose_name="ФИО")
    phone = models.CharField(max_length=30, verbose_name="Номер телефона")
    birth_date = models.DateField(verbose_name="Дата рождения", )
    education = models.CharField(max_length=100, verbose_name="Образование")
    work_place = models.CharField(max_length=200, verbose_name="Место работы")
    personal_data_agreement = models.BooleanField(default=False,
                                                  verbose_name="Согласие на обработку персональных данных")
    library_rules_agreement = models.BooleanField(default=False, verbose_name="Согласие с правилами библиотеки")
    telegram_id = models.IntegerField(verbose_name="Телеграм ID")
    date_create = models.DateTimeField(null=True, auto_now_add=True, verbose_name="Дата регистрации")

    class Meta:
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'

    def __str__(self):
        return self.name


class BookIssue(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга для выдачи")
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, verbose_name="Читатель")
    issue_date = models.DateTimeField(auto_now_add=True, verbose_name="Выдано")
    is_return = models.BooleanField(default=False, verbose_name="Книга возвращена")
    note = models.TextField(blank=True, verbose_name="Замечания")
    date_update = models.DateTimeField(null=True, auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = 'Выдача книги'
        verbose_name_plural = 'Выдачи книг'

    def __str__(self):
        return f'{self.book} - {self.reader} - {self.issue_date}'
