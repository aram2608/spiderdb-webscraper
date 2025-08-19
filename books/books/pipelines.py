# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# stdlib
import hashlib

# third party
import pymongo
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class MongoPipeline:
    COLLECTION_NAME = "books"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        """Fetches information from settings to return mongodb parameters."""
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE"),
        )

    def open_spider(self, spider):
        """Opens connection to mongodb when spider starts."""
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        """Closes mongodb connection when spider is done."""
        self.client.close()

    #def process_item(self, item, spider):
    #    """
    #    Inserts scraped items into mongodb, 
    #    Only keeping one instance no matter how many times the scraperis run.
    #    """
    #    item_id = self.compute_item_id(item)
    #    # Check to see if scraped item is unique
    #    if self.db[self.COLLECTION_NAME].find_one({"_id": item_id}):
    #        raise DropItem(f"Duplicate item found: {item}")
    #    # If item is unique save to mongodb
    #    else:
    #        item["_id"] = item_id
    #        self.db[self.COLLECTION_NAME].insert_one(ItemAdapter(item).asdict())
    #        return item

    def process_item(self, item, spider):
        """
        Inserts scraped items into mongodb, 
        Only keeping one instance no matter how many times the scraperis run.
        Auto creates db/collection on first insert
        """
        item_id = self.compute_item_id(item)
        item_dict = ItemAdapter(item).asdict()

        self.db[self.COLLECTION_NAME].update_one(
            filter={"_id": item_id},
            update={"$set": item_dict},
            upsert=True
        )

        return item

    def compute_item_id(self, item):
        """Helper method to compute number of times an item is scraped."""
        url = item["url"]
        return hashlib.sha256(url.encode("utf-8")).hexdigest()

class BooksPipeline:
    def process_item(self, item, spider):
        return item
