from RCP import Entry
from RCP import construct_entry, make_entrys_from_file, sum_times_for_tags


def test_read_entry_from_csv():
    got = make_entrys_from_file('test.csv')
    expected = [Entry(description='Test description',time=10,tags=['# sample','# tags'])]
    assert got == expected


def test_sum_hours_for_every_tag():
    tags = [
        Entry(description='Test',time=5,tags=['sample','tag']),
        Entry(description='Test2',time=5,tags=['sample','other'])
        ]
    got = sum_times_for_tags(tags)
    expected = {
        'sample' : 10,
        'tag' : 5,
        'other' : 5
        }
    assert got == expected