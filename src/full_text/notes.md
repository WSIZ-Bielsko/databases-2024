#





### trigram similarity

AI: explain Trigram Matching algorithm in postgres

- A trigram is a sequence of 3 consecutive characters from the padded word. 
- The trigrams for " hello " are {" h", " he", "hel", "ell", "llo", "lo "}.
- similarity = 2.0 * (num_shared_trigrams) / (total_trigrams_string1 + total_trigrams_string2)

- in postgres
```sql

SELECT similarity('hello', 'hell');
```


# 