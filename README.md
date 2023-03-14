# DontLectureMe

> A program that pays attention to your lectures for you.

Paying attention to a ~3h lecture is difficult, if not impossible. What if, yoru computer does it for you?

You might be thinking, "but that defeats the purpose of even being there", yes, yes it does, but some universities have mandatory attendance.

## Solution
1. You study the material before (You actually have to do this) and take notes.
2. You write down what you *do not understand*, *what you want to know more about*, and *what you want to ask the professor*.
3. You go to class, and have the computer pay attention to the lecture.
4. Once the computer recognizes a word or phrase you wrote down, it will prompt you to **pay attention**/**ask a question**/**take notes**.

## How it works
Write your notes/keywords into `keywords.txt`. Then you can run the program:

```bash
python3 main.py
```

The program will then listen to the microphone and try to recognize the keywords. If it does, it will prompt you with a notification.

## How to install

```bash
pip install -r requirements.txt
```
