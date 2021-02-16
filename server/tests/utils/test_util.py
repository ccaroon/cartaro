import faker
import time
import unittest

from cartaro.utils.util import Util
class UtilTest(unittest.TestCase):

    FAKER = faker.Faker()

    def setUp(self):
        self.FAKER.seed_instance(time.time())

    def __random_obj(self, **kwargs):
        return {
            'name': kwargs.get('name', self.FAKER.name()),
            'age': kwargs.get('age', self.FAKER.random_int(min=1, max=100)),
            'active': kwargs.get('active', self.FAKER.boolean())
        }

    def test_sort_single_key(self):
        count = 5
        data = [self.__random_obj() for i in range(count)]
        
        self.assertEqual(len(data), count)
        
        sorted_data = Util.sort(data, 'name')
        self.assertEqual(len(sorted_data), count)

        for i in range(count-1):
            self.assertLessEqual(
                sorted_data[i].get('name'),
                sorted_data[i+1].get('name') 
            )

    def test_sort_desc(self):
        count = 5
        data = [self.__random_obj() for i in range(count)]
        
        self.assertEqual(len(data), count)
        
        sorted_data = Util.sort(data, 'name:desc')
        self.assertEqual(len(sorted_data), count)

        for i in range(count-1):
            self.assertGreaterEqual(
                sorted_data[i].get('name'),
                sorted_data[i+1].get('name') 
            )

    def test_sort_multi_key(self):
        count = 6
        data = [self.__random_obj() for i in range(count)]

        # set half the objs' age to 42, the other 77
        for i, obj in enumerate(data):
            if i < (count/2):
                obj['age'] = 42
            else:
                obj['age'] = 77

        self.assertEqual(len(data), count)
        
        sorted_data = Util.sort(data, 'age,name')
        self.assertEqual(len(sorted_data), count)

        # Overall by age
        for i in range(count-1):
            self.assertLessEqual(
                sorted_data[i].get('age'),
                sorted_data[i+1].get('age') 
            )

        # Within same age by name
        for age in (42,77):
            sub_list = list(filter(lambda o: o['age'] == age, sorted_data))
            for i in range(len(sub_list)-1):
                self.assertEqual(sub_list[i].get('age'), age)
                self.assertLessEqual(
                    sub_list[i].get('name'),
                    sub_list[i+1].get('name') 
                )

    def test_sort_list_with_None(self):
        count = 5
        data = [self.__random_obj() for i in range(count)]
        
        # None vs String
        data[count-1]['name'] = None

        sorted_data = Util.sort(data, 'name')
        self.assertEqual(len(sorted_data), count)

        # None should sort to beginning
        self.assertEqual(sorted_data[0]['name'], None)
        for i in range(1, count-1):
            self.assertLessEqual(
                sorted_data[i].get('name'),
                sorted_data[i+1].get('name') 
            )

        # TODO: should probably test None with mult-key sort

        # None vs INT
        data = [self.__random_obj() for i in range(count)]
        data[count-1]['age'] = None

        sorted_data = Util.sort(data, 'age')
        self.assertEqual(len(sorted_data), count)

        # None should sort to beginning
        self.assertEqual(sorted_data[0]['age'], None)
        for i in range(1, count-1):
            self.assertLessEqual(
                sorted_data[i].get('age'),
                sorted_data[i+1].get('age') 
            )







# 
