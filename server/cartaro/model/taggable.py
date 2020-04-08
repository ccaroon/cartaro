from .tag import Tag

class Taggable:
    @property
    def tags(self):
        return self.__tags
    
    def tag(self, tag):
        if isinstance(tag, str):
            self.__tags.add(Tag(name=tag))
        elif isinstance(tag, Tag):
            self.__tags.add(tag)
        else:
            raise TypeError("'tag' must be of type `str` or `Tag`")

    def remove_tag(self, tag):
        if isinstance(tag, str):
            self.__tags.remove(Tag(name=tag))
        elif isinstance(tag, Tag):
            self.__tags.remove(tag)
        else:
            raise TypeError("'tag' must be of type `str` or `Tag`")

    def _post_save(self):
        # Add all new tags to Tag DB
        for tag in self.__tags:
            if not Tag.exists(tag.name):
                tag.save()

    def _unserialize(self, data):
        tag_list = data.get("tags", [])
        
        self.__tags = set()
        for name in tag_list:
            self.tag(name)

    def _serialize(self):
        # Store Tags that are part of the Object as strings only
        return {
            "tags": [str(tag) for tag in self.tags]
        }





# 
