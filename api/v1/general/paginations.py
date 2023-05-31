from django.core.paginator import Paginator as DjangoPaginator, EmptyPage, PageNotAnInteger


class Paginator(DjangoPaginator):
    def _init_(self, instances: list = [], count: int = 10, page: int = 1):
        super()._init_(instances, count)

        try:
            instances = self.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            instances = self.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            instances = self.page(self.num_pages)

        # pagnated objects
        self.objects = instances.object_list
        # current page number
        self.current_page = instances.number
        # total pages of instances
        self.total_pages = self.num_pages
        # total paginator items count
        self.total_items = self.count
        # index of first item in the current page
        self.first_item = instances.start_index()
        # index of last item in the current page
        self.last_item = instances.end_index()
        # has next page
        self.has_next_page = instances.has_next()
        # has previous page
        self.has_previous_page = instances.has_previous()
        # next page number
        self.next_page_number = instances.next_page_number() if self.has_next_page else None
        # previous page number
        self.previous_page_number = instances.previous_page_number() if self.has_previous_page else None

    @property
    def pagination_data(self):
        return {
            "current_page": self.current_page,
            "has_next_page": self.has_next_page,
            "next_page_number": self.next_page_number,
            "has_previous_page": self.has_previous_page,
            "previous_page_number": self.previous_page_number,
            "total_pages": self.total_pages,
            "total_items": self.total_items,
            "first_item": self.first_item,
            "last_item": self.last_item,
        }
