![logo](./vis.png)
# DontLectureMe


https://user-images.githubusercontent.com/60182044/225153948-e817307f-3ef3-4ec6-9772-558e525d3871.mp4



> A program that pays attention to your lectures for you.

Paying attention to a ~3h lecture is difficult, especially with ADHD. What if, your computer does it for you?

You might be thinking, "but that defeats the purpose of even being there", yes.

## Solution 💡
1. You study the material before (You actually have to do this) and take notes.
2. You write down what you *do not understand*, *what you want to know more about*, and *what you want to ask the professor*.
3. You go to class, and have the computer pay attention to the lecture.
4. Once the computer recognizes a word or phrase you wrote down, it will prompt you to **pay attention**/**ask a question**/**take notes**.

## Permission 📜

+ Some professors allow recording of their lectures, and some even record the lectures themselves and make them available to students.
+ However, some professors are against recording lectures because they believe it inhibits class discussion, compromises student privacy, raises intellectual property rights questions, and may encourage some students to skip attending the class.
+ Some institutions have specific policies on recording lectures. For example, the University of Rochester requires faculty members to provide lecture recordings or Zoom access to students who miss class due to illness or who need to isolate in place. It also recommends live, non-recorded Zoom access for politically charged or sensitive class discussions.
+ Recording laws vary by state. For instance, Florida is a two-party consent state, which means that both parties must consent to the recording, but courts have found that the law does not apply to recordings made in a party's place of business.
+ To avoid violating the law, it is advisable to check with the professor or consult with an experienced attorney before recording a lecture.

## How it works 🧰
Write your notes/keywords into `keywords.txt`. Then you can run the program:

```bash
python3 main.py
```

The program will then listen to the microphone and try to recognize the keywords. If it does, it will prompt you with a notification.

After the lecture, the program continuously saves the lecture into a database (sqlite) with the current date as the name, you can then use the sowing-kit to compile the lecture into a single file (audio and transcript):

```bash
python3 sowing-kit.py <date>.db
```

## How to install 📥

```bash
pip install -r requirements.txt
```
