def delete_foo(list_of_words):
    for counter, word in enumerate(list_of_words):
        if word == 'foo':
            del (list_of_words[counter])

    print('After: {}'.format(list_of_words))

#words = ['foo', 'bar', 'baz']
words = ['foo', 'foo', 'bar', 'baz']
print('Before: {}'.format(words))
delete_foo(words)
