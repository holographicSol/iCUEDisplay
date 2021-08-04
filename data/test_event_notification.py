import os


def f_1():
    with open('./event_notification_g1.dat', 'w') as fo:
        fo.writelines('True')
    fo.close()


def f_2():
    with open('./event_notification_g2.dat', 'w') as fo:
        fo.writelines('True')
    fo.close()


def f_3():
    with open('./event_notification_g3.dat', 'w') as fo:
        fo.writelines('True')
    fo.close()


def f_4():
    with open('./event_notification_g4.dat', 'w') as fo:
        fo.writelines('True')
    fo.close()


def f_5():
    with open('./event_notification_g5.dat', 'w') as fo:
        fo.writelines('True')
    fo.close()


def f_6():
    with open('./event_notification_g6.dat', 'w') as fo:
        fo.writelines('True')
    fo.close()


while True:
    print('--------------------------------')
    print('1: TEST G1           4: TEST G4')
    print('2: TEST G2           5: TEST G5')
    print('3: TEST G3           6: TEST G6')
    print('7: TEST ALL')
    print('\npress Q to quit')
    print('--------------------------------')
    x = input('?')
    if x == '1':
        f_1()
    elif x == '2':
        f_2()
    elif x == '3':
        f_3()
    elif x == '4':
        f_4()
    elif x == '5':
        f_5()
    elif x == '6':
        f_6()
    elif x == '7':
        f_1()
        f_2()
        f_3()
        f_4()
        f_5()
        f_6()
    elif x == 'Q' or x == 'q':
        break
