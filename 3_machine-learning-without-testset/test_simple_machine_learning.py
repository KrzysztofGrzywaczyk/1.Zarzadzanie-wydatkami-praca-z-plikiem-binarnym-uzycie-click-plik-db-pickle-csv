from simple_machine_lerning import count_sentiment, load_reviews, pos_neg_check, preprocess_review

def test_load_review():
    got = load_reviews("test_review.txt")
    expected = {'review': 1,'some': 1,'test': 1}
    assert got == expected

def test_sentiment_counting():
    comment="nice movie"
    pos_counter={'nice':1,'very':1}
    neg_counter={'nice':1,'very':1}
    got = count_sentiment(comment,pos_counter,neg_counter)
    assert got == 0.0

def test_split_by_every_whitespace():
    text = "Some \tfew \n words   separated"
    got = preprocess_review(text)
    expected = ["some", "few", "words", "separated"]
    assert got == expected

def test_lower_all_characters():
    text = "SaMPLe"
    got = preprocess_review(text)
    expected = ["sample"]
    assert got == expected

def test_replace_html():
    text = "some<br />words"
    got = preprocess_review(text)
    expected = ["some", "words"]
    assert got == expected

def test_replace_chars():
    text = """sample,.;':][!@#\\$%^&*"()_+-?"""
    got = preprocess_review(text)
    expected = ["sample"]
    assert got == expected

def test_positive_check():
    sentiment = 0.5
    got = pos_neg_check(sentiment)
    assert got == 'pozytywny'

def test_negative_check():
    sentiment = -0.5
    got = pos_neg_check(sentiment)
    assert got == 'negatywny'

def test_neutral_check():
    sentiment = 0.005
    got = pos_neg_check(sentiment)
    assert got == 'neutralny'