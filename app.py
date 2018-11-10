from question import Question

question_prompts = [
    "What can point in every direction but can't reach the destination by itself?\n(a) Your Finger.\n(b) Arrows\n(c) A compass\n",
    "What is the worst vegetable to have on a ship?\n(a)Broccoli\n(b)Sweetcorn\n(c)A leek\n",
    "Why was the picture sent to jail?\n(a)For picturing a crime\n(b)Because it was framed.\n(c)Evidence\n"
]

questions = [
    Question(question_prompts[0], "a"),
    Question(question_prompts[1], "c"),
    Question(question_prompts[2], "b")
]

def run_test(questions):
    score = 0
    for Question in questions:
        answer = raw_input(Question.prompt)
        if answer == Question.answer:
            score +=1
    print("You got " + str(score) + "/" + str(len(questions)) + " Correct")
    if score == len(questions):
        print("Well done You got all the riddles correct")
    
run_test(questions)