"""
Program is taking a comment from user and label it as: positive, negative or neutral
Rating is based on a set of 50 tousands real users opinions.

Usage: Just type or paste your comment!

"""

import glob


def print_intro():
    print("")
    print("--------------------------------------------------------")
    print("--------------- PROGRAM OCENY KOMENTARZA ---------------")
    print("")
    print("Ładowanie plików z recenzjami, to może potrwać kilka minut.. szczególnie przy pierwszym uruchomieniu...")
    print("")


def preprocess_review(content):
    CHARS = """,.;':][!@#\\$%^&*"()_+-?"""

    for char in CHARS:
        content = content.replace(char,"")
    review = content.lower().replace("<br />"," ").split()
    return review


def load_reviews(path:str) -> dict[str:int]:
    """Loading reviews of one type (from one path) and counting number of occurrences for each word. 
    Return dict with amount of appearance for every word."""

    files = glob.glob(path)
    counter = {}
    for file in files:
        with open(file, encoding='UTF-8') as stream:
            content = stream.read()
            review = preprocess_review(content)
            for word in set(review):
                counter[word]=counter.get(word,0) + 1
    return counter


def take_a_comment() ->str:
    """ Return taken comment in plaintext."""

    print("---------------------")
    print("")
    comment = input("Wprowadź swój komentarz do oceny (w języku angielskim): \n")
    print("")
    return comment


def count_sentiment(comment :str, pos_counter :dict[str:int], neg_counter :dict[str:int]) -> float:
    """Counting sentiments of words in -comment taking into account the number of occurrences for each word in dicts: -pos_counter and -neg_counter.
    Return sentiment of whole sentence"""

    print (pos_counter)
    
    words_in_comment = comment.lower().split()
    sentiment_sum = 0
    for word in words_in_comment:
        positive = pos_counter.get(word,0)
        negative = neg_counter.get(word,0)
        all_ = positive + negative
        if all_ != 0:                                              
            sentiment = (positive - negative) / all_                
        else:                                                          
            sentiment = 0                                           
        sentiment_sum += sentiment
        sentiment_of_sentence = sentiment_sum/len(words_in_comment)
    return sentiment_of_sentence


def pos_neg_check(sentiment_of_sentence :float) -> str:
    """Creates a label 'positive' or 'negative' based on given -sentiment_of_sentence
    Returns Label"""
    
    if sentiment_of_sentence >= 0.01:
        label = "pozytywny"
    elif sentiment_of_sentence <= -0.01:
        label = "negatywny"
    else:
        label = "neutralny"
    return label


def print_result(label :str):
    """Prints results as  label positive/negative and sentiment of whole sentence"""
    
    print ("--->")
    print("Komentarz wygląda na: ",label.upper())


def main():
    PATH_NEG = "data/aclImdb/test/neg/*.txt"
    PATH_POS = "data/aclImdb/test/pos/*.txt"

    print_intro()
    positive_counter = load_reviews(PATH_POS)
    print("Załadowano pozytywne recenzje...")
    negative_counter = load_reviews(PATH_NEG)
    print("Załadowano negatywne recenzje...")
    comment = take_a_comment()
    sentiment = count_sentiment(comment, positive_counter, negative_counter)
    label = pos_neg_check(sentiment)
    print_result(label)


if __name__ == "__main__":
    main()