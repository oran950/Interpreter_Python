from functools import reduce

#Ex 9
factorial = lambda n: reduce(lambda x, y: x * y, range(1, n + 1)) if n > 0 else 1
print(factorial(5))

#Ex 10
concat_strings = lambda strings: reduce(lambda x, y: x + ' ' + y, strings)
strings = ["Hello", "World", "Python"]
result = concat_strings(strings)
print(result)

#Ex 11
cumulative_sum_of_squares = lambda lst: list(map(lambda sublst: sum(map(lambda num: num**2, filter(lambda x: x % 2 == 0, sublst))), lst))
list_of_lists = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
result = cumulative_sum_of_squares(list_of_lists)
print(result)

#Ex 12
nums = [1, 2, 3, 4, 5, 6]
sum_squared = reduce(lambda x, y: x + y, map(lambda x: x**2, filter(lambda x: x % 2 == 0, nums)))
print(sum_squared)

#Ex 13
palindrome_counts = lambda lst: list(map(lambda sublst: reduce(lambda count, s: count + 1 if s == s[::-1] else count, filter(lambda s: isinstance(s, str) and s == s[::-1], sublst), 0), lst))


