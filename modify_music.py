#문장 입력
'''
str = ["I gotta count those words sitting on a red orange chair "
       "to check whether there's a word in a sentence which matches the keywords",
       "desk and computer is irreplacable you blue and yellow guys"]
def text_slice(texts):
    words = []
    word_start = 0
    word_end = 0
    for character in range(len(texts)):
        if character < len(texts) - 1 and texts[character] == " " and texts[character+1] != " ":
            word_start = character+1
        if (character < len(texts) - 1 and texts[character] != " " and texts[character+1] == " ") or (character == len(texts)-1 and texts[character] != " "):
            word_end = character
            words.append(texts[word_start : word_end+1])
    return words
'''

volume_modify = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
color_modify = [0, 0, 0, 0, 0, 0]

def interpret_words(words):
    doAddFrac, existingFrac, doChangeInst = 0, 0, 0
    # 명사:파편, 동사, 전치사, 형용사 등: 음색? # 복수명사 처리도 대충 하자
    keywords_fracture = ("hand", "mouth", "ear", #안경, 가위, 폰, 카메라, 타이, 벽, blurry, dark, hat
                         "glasses", "scissors", "tie",
                         "6", "7", "8",
                         "9",
                         "10",
                         "11")
    keywords_color = ("red", "blue",
                      "yellow", "black",
                      "orange", "pink",
                      "9", "10", "11",
                      "12", "13", "14",
                      "15", "16", "17")
    for word in words:
        for kf in range(len(keywords_fracture)):
            if word == keywords_fracture[kf]:
                if volume_modify[kf] == 0:
                    volume_modify[kf] = 1
                    doAddFrac = 60
                elif volume_modify[kf] == 1:
                    existingFrac = 60
        for kc in range(len(keywords_color)):
            if word == keywords_color[kc]:
                if kc<=5:
                    color_modify[kc // 2] = kc % 2
                elif kc>5:
                    color_modify[(kc-6) // 3 + 3] = (kc-6) % 3
                doChangeInst = 60
    return doAddFrac, existingFrac, doChangeInst