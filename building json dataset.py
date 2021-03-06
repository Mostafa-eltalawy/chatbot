import os
import sys
import json

import requests
import apiai
import sqlite3
import string
import urllib, json

data= {'intents': [
    {
     'tag': 'greeting',
   'patterns': ['Hi there',
    'How are you',
    'Is anyone there?',
    'Hey',
    'Hola',
    'Hello',
    'Good day'],
   'responses': ['Hello, thanks for asking',
    'Good to see you again',
    'Hi there, how can I help?'],
   'context': ['']
   },
             
  {
   'tag': 'goodbye',
   'patterns': ['Bye',
    'See you later',
    'Goodbye',
    'Nice chatting to you, bye',
    'Till next time'],
   'responses': ['See you!', 'Have a nice day', 'Bye! Come back again soon.'],
   'context': ['']
   },
  
  {
   'tag': 'thanks',
   'patterns': ['Thanks',
    'Thank you',
    "That's helpful",
    'Awesome, thanks',
    'Thanks for helping me'],
   'responses': ['Happy to help!', 'Any time!', 'My pleasure'],
   'context': ['']
   },
  
  {
   'tag': 'noanswer',
   'patterns': [],
   'responses': ["Sorry, can't understand you",
    'Please give me more info',
    'Not sure I understand'],
   'context': ['']
   },
  
  {
   'tag': 'options',
   'patterns': ['How you could help me?',
    'What you can do?',
    'What help you provide?',
    'How you can be helpful?',
    'What support is offered'],
   'responses': ['What are you experiencing?  \n\n High blood pressure (hypertension) \n or Skin and eyes that appear yellowish \n or fever \n or Pain in the neck, jaw, throat, upper abdomen or back  \n please write all what you feel one time !! '],
   'context': ['']
   },
  
  {
   'tag': 'kidney_disease',
   'patterns': ['Nausea',
                'Vomiting',
                'Loss of appetite',
                'Fatigue and weakness',
                'Sleep problems',
                'Changes in how much you urinate',
                'Decreased mental sharpness',
                'Muscle twitches and cramps',
                'Swelling of feet and ankles',
                'Persistent itching',
                'Chest pain, if fluid builds up around the lining of the heart',
                'Shortness of breath, if fluid builds up in the lungs',
                'High blood pressure (hypertension) that is difficult to control'],
   'responses': ['Ok, sir. You are suffering from kidney disease. \n to show the doctor list write (kidney Doctors )\n and please choose one'],
   'context': ['']
   },

  {
   'tag': 'liver_disease',
   'patterns': ['Skin and eyes that appear yellowish (jaundice)',
                'Abdominal pain and swelling',
                'Swelling in the legs and ankles',
                'Itchy skin',
                'Dark urine color',
                'Pale stool color',
                'Chronic fatigue',
                'Nausea or vomiting',
                'Loss of appetite',
                'Tendency to bruise easily'],
   'responses': ['Ok, sir. You are suffering from liver disease. \n to show the doctor list write (liver Doctors )\n and please choose one'],
   'context': ['']
   },

  {
   'tag': 'covid-19_disease',
   'patterns': ['fever',
                'dry cough',
                'tiredness',
                'aches and pains',
                'sore throat',
                'diarrhea',
                'conjunctivitis',
                'headache',
                'loss of taste or smell',
                'rash on skin',
                'discoloration of fingers or toes',
                'difficulty breathing or shortness of breath',
                'chest pain or pressure',
                'loss of speech or movement'],
   'responses': ['Ok, sir. You are suffering from covid-19 disease. \n to show the doctor list write (covid-19 Doctors )\n and please choose one'],
   'context': ['']
   },


  {
   'tag': 'heart_disease_in_blood_vessels',
   'patterns': ['Chest pain',
                'chest tightness',
                'chest pressure',
                'chest discomfort (angina)',
                'Shortness of breath',
                'Pain, numbness, weakness or coldness in your legs or arms if the blood vessels in those parts of your body are narrowed',
                'Pain in the neck, jaw, throat, upper abdomen or back'],
   'responses': ['Ok, sir. You are suffering from heart disease in your blood vessels. \n to show the doctor list write (heart Doctors )\n and please choose one'],
   'context': ['']
   },

  {
   'tag': 'Heart_disease_symptoms_caused_by_abnormal_heartbeats_heart_arrhythmias',
   'patterns': ['Fluttering in your chest',
                'Racing heartbeat (tachycardia)',
                'Slow heartbeat (bradycardia)',
                'Chest pain or discomfort',
                'Shortness of breath',
                'Lightheadedness',
                'Dizziness',
                'Fainting (syncope) or near fainting'],
   'responses': ['Ok, sir. You are suffering from Heart disease symptoms caused by abnormal heartbeats (heart arrhythmias). \n to show the doctor list write (heart Doctors )\n and please choose one'],
   'context': ['']
   },


  {
   'tag': 'Heart_disease_symptoms_caused_by_heart_infections',
   'patterns': ['Fever',
                'Shortness of breath',
                'Weakness or fatigue',
                'Swelling in your legs or abdomen',
                'Changes in your heart rhythm',
                'Dry or persistent cough',
                'Skin rashes or unusual spots'],
   'responses': ['Ok, sir. You are suffering from Heart disease symptoms caused by heart infections. \n to show the doctor list write (heart Doctors )\n and please choose one'],
   'context': ['']
   },


  {
   'tag': 'Heart_disease_symptoms_caused_by_valvular_heart_disease',
   'patterns': ['Fatigue',
                'Shortness of breath',
                'Irregular heartbeat',
                'Swollen feet or ankles',
                'Chest pain',
                'Fainting (syncope)'],
   'responses': ['Ok, sir. You are suffering from Heart disease symptoms caused by valvular heart disease. \n to show the doctor list write (heart Doctors )\n and please choose one'],
   'context': ['']
   },

  {
   'tag': 'liver_disease_Doctors',
   'patterns': ['liver Doctors'],
   'responses': ['liver disease Doctors list...\n please choose one : \
                 \n 1. Dr Karim Ahmed Elsayed \n Date:Sunday,Tuseday & Friday from 12:05 pm to 10:00 pm  \
                 \n 2. Dr. Ehab Saleh \n Date:Every Day from 11:00 am to 08:00 pm \
                 \n 3. Dr. Mohamed Abdelaziz \n Date: Wednesday,Thursday & Friday  from 10:00 am to 09:00 pm \
                 \n 4. Dr. Mostafa Hamada \n Date: Every Day from 02:00 pm to 09:00 pm \
                 \n 5. Dr. Souzy Kamal \n Date: Every Day from 04:00 pm to 11:00 pm '],
   'context': ['']
   }, 

  {
   'tag': 'Heart_disease_Doctors',
   'patterns': ['Heart Doctors'],
   'responses': ['Heart disease Doctors list...\n please choose one : \
                 \n 1. Dr Mahmoud Shehab \n Date: Every Day Except Friday from 10:00 am to 06:00 pm  \
                 \n 2. Dr. Mai Fathy \n Date: Every Day from 11:00 am to 05:00 pm \
                 \n 3. Dr.Karim Sobhy \n Date: Saterday ,Monday & Thursday from 10:00 am to 10:00 pm \
                 \n 4. Dr.Islam Sobhy \n Date: Every Day from 09:00 am to 08:00 pm \
                 \n 5. Dr.Hagar Mohamed \n Date: Sunday ,Wednesday & Thursday from 12:05 pm to 06:00 pm '],
   'context': ['']
   },                 
                 
  {
   'tag': 'kidney_disease_Doctors',
   'patterns': ['kidney Doctors '],
   'responses': ['kidney disease Doctors list... \n please choose one : \
                 \n 1. Dr Mohamed Ibrahim Atef \n Date: Every Day from 02:00 pm to 08:00 pm  \
                 \n 2. Dr. Omar Mansour \n Date: Friday & Saterday from 02:00 pm to 10:00 pm \
                 \n 3. Dr.Saleh Mohamed \n Date: Saterday ,Tuseday & Thursday from 03:00 pm to 10:00 pm \
                 \n 4. Dr.Ahmed Mahmoud \n Date: Sunday,Monday & Tuseday from 02:00 pm to 11:30 pm \
                 \n 5. Dr.Gamal Karim Hafez \n Date: Monday,Thursday,Wednesday & Thursday from 03:00 pm to 08:00 pm '],
   'context': ['']
   }, 

  {
   'tag': 'kidney_Doctors',
   'patterns': [''],
   'responses': ['kidney disease Doctors list... \n please choose one : \
                 \n 1. Dr Mohamed Ibrahim Atef \n Date: Every Day from 02:00 pm to 08:00 pm  \
                 \n 2. Dr. Omar Mansour \n Date: Friday & Saterday from 02:00 pm to 10:00 pm \
                 \n 3. Dr.Saleh Mohamed \n Date: Saterday ,Tuseday & Thursday from 03:00 pm to 10:00 pm \
                 \n 4. Dr.Ahmed Mahmoud \n Date: Sunday,Monday & Tuseday from 02:00 pm to 11:30 pm \
                 \n 5. Dr.Gamal Karim Hafez \n Date: Monday,Thursday,Wednesday & Thursday from 03:00 pm to 08:00 pm '],
   'context': ['']
   }, 
                 
  {
   'tag': 'covid-19_Doctors',
   'patterns': ['covid-19 Doctors'],
   'responses': ['covid-19 Doctors list...\n please choose one : \
                 \n 1. Dr Mostafa Fathi Kamel ,\n Date: Saterday,Sunday & Tuseday from 11:00 am to 09:00 pm  \
                 \n 2. Dr. Moaaz Ayman \n Date: Sunday & Monday from 09:00 am to 06:00 pm \
                 \n 3. Dr.Nagla Elshabory \n Date: Every Days Except Friday & Saterday from 06:00 pm to 09:00 pm \
                 \n 4. Dr.Refat Ali \n Date: All Days Except Friday from 10:00 am to 06:00 pm \
                 \n 5. Dr.Mohamed Mansour \n Date: Saterday ,Monday , Thursday & Friday from 04:00 pm to 11:00 pm '],
   'context': ['']
   },    
    
  {
   'tag': 'confirm_the_detention',
   'patterns': ['Confirm Confirmed ok',
                'Mostafa Fathi Kamel  Moaaz Ayman Nagla Elshabory Refat Ali Mohamed Mansour',
                'Mohamed Ibrahim Atef Omar Mansour Saleh Mohamed Ahmed Mahmoud Gamal Karim Hafez',
                'Mahmoud Shehab Mai Fathy Karim Sobhy Islam Sobhy Hagar Mohamed ',
                ' Karim Ahmed Elsayed Ehab Saleh Mohamed Abdelaziz Mostafa Hamada Souzy Kamal' ],
   'responses': ['Ok, Thank you. \n you will contact with this doctor as per his date, \n we will send  you a notification 2 hours before. '],
   'context': ['']
   },

  {
   'tag': 'refuse_the_detention',
   'patterns': ['Refused no'],
   'responses': ['Ok,\n we will check our doctors schedule and contact you .. \n Thanks you.'],
   'context': ['']
   },
  
  ]
}



# the json file where the output must be stored 
out_file = open("intents.json", "w") 
  
json.dump(data, out_file, indent = 6) 
  
out_file.close()
