# animal_guessing
This is the technical assignment accomplished by Kirill Semenov. The aim was to create a chatbot (with use of Dialogflow framework) that plays animal guessing game. </br>
**The link to the demo of the bot:** : https://bot.dialogflow.com/7f2425b2-bde5-4ed2-9579-cecbc04bb9c3 
</br>
**How to play**
1. As the Dialogflow allows only for the detection and answering for the intents, the user should start the dialog (by standard greetings like "hi", "hello" etc.)
2. The user can either guess the animal, or get new info by asking leading questions. The questions about the animal can either be formed as "yes/no" questions ("does it have 4 legs? => {y; n}), or by requesting the infromation about the animal ("how many legs does the animal have?" => {number of legs}). When the user guesses the animal right, he is provided by the opportunity to repeat the game. The user can also exit the game at any step (before the beginning, within the game and after it).
</br>
**Code description**

1. The [code](animal_guessing.py) and the [intents](animal_guessing.zip) are organized as follows:
 * after `start` intent, the agent imports the [`animals.csv`](animals.csv) file with the information about the animals and picks a random animal (functions `making_dataset` and `taking_random_animal`). Until the animal is guessed correctly, it is fixed as a global variable.
 *  the `guess_PARAM` (where PARAM is a parameter from the dataset) intents are aimed at catching the user's hypotheses about the animal's features. They are processed by `process_PARAM` functions within the back-end. The `request_PARAM` intents are aimed at giving explicit hints to the user (processed by `get_hint` function).  
 *  both system entities (such as `@sys.color`) and the custom entities are used in the flow. The aim of the custom entities (such as `num_legs` or `underwater`) is to catch the various synonimous values and compare them to unique values in the dataset. 

2. For providing the access to the Dialogflow and Heroku of my project, please send me your email addresses. Meanwhile, the copies and backups of to the codes are provided below:
</br> 

| File | description |
| --- | --- |
| [animal_guessing.py](animal_guessing.py) | the main code with the dialog system |
| [animal_guessing.zip](animal_guessing.zip) | the backup with the intents, entities and other elements of the Dialogflow framework |
| [animals.csv](animals.csv) | the dataset with the animals and their parameters |
| [requirements.txt](requirements.txt), [Procfile](Procfile) | parameters and configurations necessary for the heroku deployment of the chatbot |

