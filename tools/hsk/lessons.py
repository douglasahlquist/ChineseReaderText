# Sample HSK 1 lessons. Words inside a sentence are separated by spaces (speak=word);
# names (大明, 小月, 小明) are allowed anywhere.
NAMES = {"大明": "Dà míng", "小月": "Xiǎo yuè", "小明": "Xiǎo míng"}

LESSONS = [
  {
    "file": "01-ni-hao.md",
    "title": ("第一课：你好", "Lesson 1: Hello"),
    "words": [
      ("好", "good; well; OK", [
        ("好。", "Good. / OK."),
        ("好， 好。", "OK, OK."),
        ("好！", "Great!"),
      ]),
      ("你", "you", [
        ("你 好！", "Hello! (literally “you good”)"),
        ("你 好， 你 好！", "Hello, hello!"),
        ("你？", "You?"),
      ]),
      ("我", "I; me", [
        ("我？", "Me?"),
        ("我 好。", "I'm well."),
        ("你 好！ 我 好。", "Hello! I'm well."),
      ]),
      ("是", "to be; yes", [
        ("是。", "Yes. (That's right.)"),
        ("是 我。", "It's me."),
        ("是 你！", "It's you!"),
      ]),
      ("叫", "to be called; to call", [
        ("我 叫 大明。", "My name is Daming. (I'm called Daming.)"),
        ("你 叫 小月。", "Your name is Xiaoyue."),
        ("是， 我 叫 小月。", "Yes, my name is Xiaoyue."),
      ]),
      ("什么", "what", [
        ("什么？", "What?"),
        ("你 叫 什么？", "What are you called?"),
        ("我 叫 大明， 你 叫 什么？", "I'm called Daming. What are you called?"),
      ]),
      ("的", "(possessive particle) 's; of", [
        ("我 的。", "Mine."),
        ("是 你 的。", "It's yours."),
        ("是 我 的， 好！", "It's mine, great!"),
      ]),
      ("名字", "name", [
        ("你 叫 什么 名字？", "What is your name?"),
        ("我 的 名字 是 小月。", "My name is Xiaoyue."),
        ("你 的 名字 是 什么？", "What is your name? (What is your name called?)"),
      ]),
      ("再见", "goodbye", [
        ("再见！", "Goodbye!"),
        ("大明， 再见！", "Bye, Daming!"),
        ("好， 再见！", "OK, goodbye!"),
      ]),
    ],
    "dialogs": [
      [("A", "你 好！", "Hello!"),
       ("B", "你 好！", "Hello!"),
       ("A", "我 叫 大明。 你 叫 什么 名字？", "I'm Daming. What's your name?"),
       ("B", "我 叫 小月。", "I'm Xiaoyue.")],
      [("A", "你 是 大明？", "You're Daming?"),
       ("B", "是， 我 是 大明。", "Yes, I'm Daming."),
       ("A", "我 的 名字 是 小月。", "My name is Xiaoyue."),
       ("B", "小月， 你 好！", "Hello, Xiaoyue!")],
      [("A", "你 好， 我 是 小月。", "Hello, I'm Xiaoyue."),
       ("B", "你 好， 小月！ 我 叫 大明。", "Hello, Xiaoyue! I'm called Daming."),
       ("A", "大明， 再见！", "Goodbye, Daming!"),
       ("B", "再见！", "Goodbye!")],
    ],
  },
  {
    "file": "02-ni-hao-ma.md",
    "title": ("第二课：你好吗", "Lesson 2: How are you?"),
    "words": [
      ("吗", "(question particle for yes/no questions)", [
        ("你 好 吗？", "How are you? (Are you well?)"),
        ("你 是 大明 吗？", "Are you Daming?"),
        ("你 叫 小月 吗？", "Is your name Xiaoyue?"),
      ]),
      ("很", "very; quite", [
        ("很 好。", "Very good."),
        ("我 很 好。", "I'm very well."),
        ("你 的 名字 很 好。", "Your name is very nice."),
      ]),
      ("也", "also; too", [
        ("我 也 很 好。", "I'm very well too."),
        ("我 也 叫 大明！", "My name is Daming too!"),
        ("你 也 叫 小月 吗？", "Is your name Xiaoyue too?"),
      ]),
      ("不", "not; no", [
        ("不 是。", "No. (It isn't.)"),
        ("我 不 是 大明。", "I'm not Daming."),
        ("我 不 叫 小月， 我 叫 小明。", "My name isn't Xiaoyue, it's Xiaoming."),
      ]),
      ("呢", "(particle) and …? what about …?", [
        ("你 呢？", "And you?"),
        ("我 很 好， 你 呢？", "I'm very well, and you?"),
        ("我 叫 大明， 你 呢？", "I'm Daming, and you?"),
      ]),
      ("他", "he; him", [
        ("他 是 大明。", "He is Daming."),
        ("他 叫 什么 名字？", "What's his name?"),
        ("他 也 很 好。", "He's very well too."),
      ]),
      ("她", "she; her", [
        ("她 是 小月。", "She is Xiaoyue."),
        ("她 好 吗？", "How is she?"),
        ("她 不 叫 小月 吗？", "Isn't her name Xiaoyue?"),
      ]),
      ("谢谢", "thank you; thanks", [
        ("谢谢！", "Thanks!"),
        ("谢谢 你！", "Thank you!"),
        ("我 很 好， 谢谢！", "I'm very well, thanks!"),
      ]),
      ("不客气", "you're welcome", [
        ("不客气！", "You're welcome!"),
        ("不客气， 再见！", "You're welcome, goodbye!"),
        ("谢谢 你！ —— 不客气。", "Thank you! — You're welcome."),
      ]),
    ],
    "dialogs": [
      [("A", "你 好 吗？", "How are you?"),
       ("B", "我 很 好， 谢谢！ 你 呢？", "I'm very well, thanks! And you?"),
       ("A", "我 也 很 好。", "I'm very well too.")],
      [("A", "他 是 大明 吗？", "Is he Daming?"),
       ("B", "不 是， 他 不 是 大明。", "No, he isn't Daming."),
       ("A", "他 叫 什么 名字？", "What's his name?"),
       ("B", "他 叫 小明。", "His name is Xiaoming.")],
      [("A", "你 好！ 你 是 小月 吗？", "Hello! Are you Xiaoyue?"),
       ("B", "是， 我 是 小月。 你 呢？", "Yes, I'm Xiaoyue. And you?"),
       ("A", "我 叫 大明。 谢谢 你， 小月！", "I'm Daming. Thank you, Xiaoyue!"),
       ("B", "不客气！ 再见！", "You're welcome! Goodbye!")],
    ],
  },
  {
    "file": "03-wo-de-pengyou.md",
    "title": ("第三课：我的朋友", "Lesson 3: My friends"),
    "words": [
      ("这", "this", [
        ("这 是 大明。", "This is Daming."),
        ("这 是 我。", "This is me."),
        ("这 是 什么？", "What is this?"),
      ]),
      ("那", "that", [
        ("那 是 小月。", "That's Xiaoyue."),
        ("那 是 什么？", "What's that?"),
        ("那 是 你 的 吗？", "Is that yours?"),
      ]),
      ("一", "one", [
        ("一。", "One."),
        ("一， 一， 一。", "One, one, one."),
        ("是 一 吗？", "Is it one?"),
      ]),
      ("个", "(measure word for people and many things)", [
        ("一 个。", "One (of them)."),
        ("这 个 是 什么？", "What is this one?"),
        ("那 个 是 你 的 吗？", "Is that one yours?"),
      ]),
      ("人", "person; people", [
        ("一 个 人。", "One person. / Alone."),
        ("那 个 人 是 大明。", "That person is Daming."),
        ("那 个 人 叫 什么 名字？", "What's that person's name?"),
      ]),
      ("朋友", "friend", [
        ("他 是 我 的 朋友。", "He is my friend."),
        ("这 是 我 的 朋友 小月。", "This is my friend Xiaoyue."),
        ("你 的 朋友 叫 什么 名字？", "What's your friend's name?"),
      ]),
      ("我们", "we; us", [
        ("我们 是 朋友。", "We are friends."),
        ("我们 很 好。", "We're very well."),
        ("我们 也 是 朋友 吗？", "Are we friends too?"),
      ]),
      ("你们", "you (plural)", [
        ("你们 好！", "Hello, everyone!"),
        ("你们 是 朋友 吗？", "Are you friends?"),
        ("你们 好 吗？", "How are you all?"),
      ]),
      ("他们", "they; them", [
        ("他们 是 我 的 朋友。", "They are my friends."),
        ("他们 也 很 好。", "They're very well too."),
        ("他们 叫 什么 名字？", "What are their names?"),
      ]),
      ("有", "to have; there is", [
        ("我 有 一 个 朋友。", "I have a friend."),
        ("你 有 朋友 吗？", "Do you have friends?"),
        ("他 有 一 个 朋友 叫 大明。", "He has a friend named Daming."),
      ]),
      ("没有", "not have; there isn't", [
        ("没有。", "No. (I don't have one.)"),
        ("我 没有。", "I don't have one."),
        ("他 有， 我 没有。", "He has one; I don't."),
      ]),
    ],
    "dialogs": [
      [("A", "这 是 我 的 朋友 小月。", "This is my friend Xiaoyue."),
       ("B", "你 好， 小月！ 我 叫 大明。", "Hello, Xiaoyue! I'm Daming."),
       ("A", "大明 也 是 我 的 朋友。", "Daming is my friend too."),
       ("B", "我们 是 朋友！", "We're friends!")],
      [("A", "那 个 人 是 你 的 朋友 吗？", "Is that person your friend?"),
       ("B", "是， 他 叫 小明。", "Yes, his name is Xiaoming."),
       ("A", "他 也 是 我 的 朋友！", "He's my friend too!"),
       ("B", "是 吗？", "Really?")],
      [("A", "你们 好！ 你们 是 朋友 吗？", "Hello! Are you friends?"),
       ("B", "是， 我们 是 朋友。", "Yes, we're friends."),
       ("A", "你们 叫 什么 名字？", "What are your names?"),
       ("B", "我 叫 大明， 她 叫 小月。 你 呢？", "I'm Daming, and she's Xiaoyue. And you?"),
       ("A", "我 叫 小明。 再见！", "I'm Xiaoming. Goodbye!")],
    ],
  },
]
