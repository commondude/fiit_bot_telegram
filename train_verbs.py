import requests as rq
import json
import random


def translate(txt):
    r = rq.post('https://translate.yandex.net/api/v1.5/tr.json/translate', data={
        'key': 'trnsl.1.1.20200416T130658Z.adb21a55e704afd6.c839dff4f9baf67fb6a528a45f8bd37711e64610',
        'text': txt, 'lang': 'ru', 'format': 'plain'})
    json_loaded = json.loads(r.text)
    print(json_loaded)
    try:
        text = json_loaded['text'][0]
    except:
        text = "Smthng wrng"
    return  text



def rand_sentence():
    verbs=[]
    f=open('verbs.txt','r', encoding='utf8')
    for line in f:
        verbs.append(line.split())
    f.close()
    verb=random.choice(verbs)

    face_list = ['He', 'She', 'It', 'We', 'They', 'I', 'You']
    times_list = ['Past', 'Present', 'Future']
    nsq_list = ['Negation', 'Statement', 'Question']
    past_nsq_list = ['Did not','','Did']
    present_nsq_list =['Do not','','Do']
    future_nsq_list =['Will not','Will','Will']


    face = random.choice(face_list)
    cur_time = random.choice(times_list)
    cur_nsq = random.choice(nsq_list)
    sentence= ''
    error=False

    if cur_nsq=='Question':
        if cur_time=='Past':
            sentence += 'Did '+face+' '+verb[0]+'?'
        elif cur_time=='Present':
            if face_list.index(face)>2:
                sentence += 'Do '+face+' '+verb[0]+'?'
            else:
                sentence += 'Does '+face+' '+verb[0]+'?'
        elif cur_time=='Future':
            sentence += 'Will '+face+' '+verb[0]+'?'
        else:
            error='Error in Questions time'
    elif cur_nsq=='Negation':
        sentence = face
        if cur_time == 'Past':
            sentence += ' Did not '+verb[1]+'.'
        elif cur_time == 'Present':
            if face_list.index(face)>2:
                sentence +=' Do not '+verb[0]+'.'
            else:
                sentence += ' Does not' + verb[0]+'.'

        elif cur_time == 'Future':
            sentence += ' Will not '+ verb[0]+'.'
        else:
            sentence = 'Error in Negation time'
    elif cur_nsq=='Statement':
        sentence=face
        if cur_time=='Past':
            sentence += ' '+verb[1]+'.'
        elif cur_time=='Present':
            if face_list.index(face)>2:
                sentence +=' '+verb[0]+'.'
            else:
                sentence += ' '+verb[0]+'s.'

        elif cur_time=='Future':
            sentence += ' Will '+verb[0]+'.'
        else:
            error='Error in Statement time'
    else:
        error='Error i nsq'

    return [sentence,error]



# print('Number of verbs is = '+str(len(verbs)))


# print(verb)
# print('Current verb is "'+verb[0]+'" translate as "'+verb[-1]+'"')
# rd_sen=rand_sentence(verb)
#
# if not rd_sen[1]:
#     print('Rand sentence is "'+rd_sen[0]+'"')
#     print(translate(rd_sen[0]))
# else:
#     print(rd_sen[1])







# 'Will' 'not"
# 'Do' 'Did' 'Does'


#txt = random.choice()
