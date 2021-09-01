from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class MyClass(Base):
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    first_column = Column(String)
    second_column = Column(String)
    box = Column(Integer)
Base.metadata.create_all(engine)

result_list = session.query(MyClass).all()

def main_menu():
    #
    print("1. Add flashcards")
    print("2. Practice flashcards")
    print("3. Exit")
    #
    user_input1 = input()
    #
    try:
        user_input1 = int(user_input1)
    except:
        pass
    #
    if (user_input1) == 1:
        sub_menu()
        main_menu()
    elif (user_input1) == 2:
        practice()
    elif (user_input1) == 3:
        print("Bye!")
    else:
        print (str(user_input1) + " is not an option")
        main_menu()
    #

def sub_menu():
    print("1. Add a new flashcard")
    print("2. Exit")
    user_input2 = input()

    try:
        user_input2 = int(user_input2)
    except:
        pass

    if (user_input2) == 1:
        add_flashcard()

    elif (user_input2) == 2:
        pass

    else:
        print (str(user_input2) + " is not an option")
        sub_menu()

flashcards = {}
def add_flashcard():
    print("Question:")
    question = input()
    while (len(question.replace(' ',"")) == 0):
        print("Question:")
        question = input()
    print("Answer:")
    answer = input()
    while (len(answer.replace(' ',"")) == 0):
        print("Answer:")
        answer = input()
    flashcards[question] = answer
    new_data = MyClass(first_column=question, second_column=answer, box=1)
    session.add(new_data)
    session.commit()
    sub_menu()

def practice():
    result_list = session.query(MyClass).all()
    if len(result_list) == 0:
        print("There is no flashcard to practice!")
        main_menu()
        return #used to break out of function

    for i in range(len(result_list)):
        print("")
        print("Question: " + result_list[i].first_column)
        identity = result_list[i].id
        print('press "y" to see the answer:')
        print('press "n" to skip:')
        print('press "u" to update:')

        yes_or_no = input().strip(" ")

        if (yes_or_no.strip(" ") == 'y'):
            print("")
            print("Answer: " + result_list[i].second_column)
            learning_menu(identity)
        elif (yes_or_no.strip(" ") == 'n'):
            learning_menu(identity)
        elif (yes_or_no.strip(" ") == 'u'):
            update(identity)
        else:
            print (str(user_input1) + " is not an option")
            practice()
    main_menu()

def update(identity):
    print('press "d" to delete the flashcard:')
    print('press "e" to edit the flashcard:')
    delete_or_edit = input().strip(" ")
    if (delete_or_edit == 'd'):
        session.query(MyClass).filter(MyClass.id == identity).delete()
        session.commit()
    elif (delete_or_edit == 'e'):
        for question in session.query(MyClass.first_column).filter(MyClass.id == identity):
            print("current question: " + str(question[0]))

        print("please write a new question:")
        question_update = str(input())
        for answer in session.query(MyClass.second_column).filter(MyClass.id == identity):
            print("current answer: " + str(answer[0]))
        print("please write a new answer:")
        answer_update = str(input())
        test_q = question_update.strip(" ")
        test_a = answer_update.strip(" ")
        if (test_q and test_a):
            session.query(MyClass).filter(MyClass.id == identity).\
                update({'first_column':question_update,'second_column':answer_update})
            session.commit()
    else:
        print (str(delete_or_edit) + " is not an option")
        sub_menu()
        update(identity)

def learning_menu(identity):
    print('press "y" if your answer is correct:')
    print('press "n" if your answer is wrong:')
    learn_tally = input().strip(" ")
    if (learn_tally  == 'y'):
        for tally in session.query(MyClass.box).filter(MyClass.id == identity):
            if tally[0] < 3:
                tally_copy = tally[0] + 1
                session.query(MyClass).filter(MyClass.id == identity).\
                update({'box':tally_copy})
                session.commit()
            if tally[0] == 3:
                session.query(MyClass).filter(MyClass.id == identity).delete()
                session.commit()
    elif (learn_tally == 'n'):
        for tally in session.query(MyClass.box).filter(MyClass.id == identity):
            if tally[0] < 3 and tally[0] > 1:
                tally_copy = tally[0] - 1
                session.query(MyClass).filter(MyClass.id == identity).\
                update({'box': tally_copy})
                session.commit()
    else:
        learning_menu(identity)

main_menu()
