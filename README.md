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
