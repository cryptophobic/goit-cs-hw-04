# 1. Реалізація багатопотокового підходу до обробки файлів (використовуючи threading):

Розділіть список файлів між різними потоками.
Кожен потік має шукати задані ключові слова у своєму наборі файлів.
Зберіть і виведіть результати пошуку з усіх потоків.

Для пошуку я взяв описи найвідоміших лісів у світі.

Ключові слова "trees", "beauty", "green", "species"

Результат виконання

```
Ключове слово: species, кількість файлів: 10
	./files/Congolian.txt
	./files/Monteverde.txt
	./files/Olympic.txt
	./files/Arashiyama.txt
	./files/Ardennes.txt
	./files/Schwarzwald.txt
	./files/Amazonia.txt
	./files/Rata.txt
	./files/Redwood.txt
	./files/Daintree.txt

Ключове слово: trees, кількість файлів: 6
	./files/Monteverde.txt
	./files/Olympic.txt
	./files/Schwarzwald.txt
	./files/Amazonia.txt
	./files/Rata.txt
	./files/Redwood.txt

Ключове слово: beauty, кількість файлів: 6
	./files/Olympic.txt
	./files/Arashiyama.txt
	./files/Ardennes.txt
	./files/Schwarzwald.txt
	./files/Redwood.txt
	./files/Daintree.txt

Повний час виконання 0.007528066635131836s
Сумарний час виконання потоків 0.021332979202270508s
Паралельне виконання заощадило нам 0.013804912567138672s
```

# 2. Реалізація багатопроцесорного підходу до обробки файлів (використовуючи multiprocessing):

Розділіть список файлів між різними процесами.
Кожен процес має обробляти свою частину файлів, шукаючи ключові слова.
Використайте механізм обміну даними (наприклад, через Queue) для збору та виведення результатів пошуку.

Для пошуку я взяв описи найвідоміших лісів у світі.
Ключові слова "trees", "beauty", "green", "species"

Результат виконання.

```
Ключове слово: trees, кількість файлів: 6
	./files/Monteverde.txt
	./files/Amazonia.txt
	./files/Schwarzwald.txt
	./files/Redwood.txt
	./files/Olympic.txt
	./files/Rata.txt

Ключове слово: species, кількість файлів: 10
	./files/Monteverde.txt
	./files/Amazonia.txt
	./files/Congolian.txt
	./files/Ardennes.txt
	./files/Schwarzwald.txt
	./files/Daintree.txt
	./files/Arashiyama.txt
	./files/Redwood.txt
	./files/Olympic.txt
	./files/Rata.txt

Ключове слово: beauty, кількість файлів: 6
	./files/Ardennes.txt
	./files/Schwarzwald.txt
	./files/Daintree.txt
	./files/Arashiyama.txt
	./files/Redwood.txt
	./files/Olympic.txt

Повний час виконання 0.20988702774047852s
Сумарний час виконання процесів 0.012584447860717773s
Паралельне виконання заощадило нам -0.19730257987976074s
```

Паралельне виконання не заощадило нам часу в даному конкретному випадку.

Мабуть, накладні витати на створення та видалення процесу виявились дорожчі за паралельний пошук 4-х слів по досить маленьким файлам.

