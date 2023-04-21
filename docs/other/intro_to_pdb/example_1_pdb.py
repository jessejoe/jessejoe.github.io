def delete_foo(list_of_words):
    for counter, word in enumerate(list_of_words):
        if word == 'foo':
            del (list_of_words[counter])

    print(list_of_words)


delete_foo(['foo', 'bar', 'baz'])
#delete_foo(['foo', 'foo', 'bar', 'baz'])
