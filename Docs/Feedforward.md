# Project Information

**FIRST & LAST NAME:** Mykyta Tsykunov

**Sparring Partner:** Danylo Bordunov

**Project Summary in max 10 words:** Face authentication program allows users to login the study platform

**Project Title:** FaceAuth

# Feedforward Conversations

### Week 1

## Conversation 1 (Date: 23/05/2024)

Lecturer: Marie

Questions for this conversation:

- [x] What to start with?

This is the feedback on my questions.

- Feedback 1: I have consultation with **Marie**, where we have discussed my plan for training my AI model, she said that I could try to make the face detecton model first, get accuracy above 90% and then start my face recognition.

## Conversation 2 (Date: 24/05/2024)

Lecturer: Frederik

Questions for this conversation:

- [x] Question 1: I want to talk to my database in my app.py, what are the possible ways to do it?

This is the feedback on my questions.

- Feedback 1: I spoke to **Frederik**, we have discussed how my database would look like and how to connect to it, he said he will send me some guides on how to implement mySQL database in python.

## Conversation 3 (Date: 24/05/2024)

Lecturer: Tijn

Questions for this conversation:

- [x] Question 1: How to create a layout for my box?

This is the feedback on my questions.

- Feedback 1: I was talking with **Tijn** about my maker part, where I will use some plywood and apply laser cutting on it, I made another consultation, because I want some help to make a pdf file for laser cutting, so I can come and cut the pieces of my box.

### Week 2

## Conversation 4 (Date: 27/05/2024)

Lecturer: Christophe

Questions for this conversation:

- [x] Question 1: I want to make a web page in python, what can I use for that?

This is the feedback on my questions.

- Feedback 1: I have an a consultation with **Christophe**, my idea was to create some sort of web service, but it turned out to be a very difficult task for the first project. Because I wanted to use a webapp, MySQL database, my AI model and raspi all at once. Christophe advised to create some separate scripts, for instance: I run the script signup.py to sign up and save the user to the database, then run script for recording user's face and train face recognition model. And last but not least I run my app.py, connect to my raspi and do face authentication, if the authentication ends up successfully, It will show a welcome message on an LCD Display. The problem is I wanted all these "actions" to be in my webapp, so I needed some web service to connect to my model and send some images(don't forget that we need talk to raspi from this web service as well), and that is the topic of the 2nd year of MCT CT&AI. He sent me an example of Flask website, I'm going to use it to create a simple form page, where you can sign up and your data will be saved in MySQL database.

## MVP01: annotated data (Date: 28/05/2024)

I showed my dataset, I said it was not really good, because my accuracy was relatively low, so I ask if I can use another dataset. Marie respond it's possible if my model is working really poorly. I explaind what is my plan for my project one: I want to create a small flask website, so I can use database to store users and add a new one. I showed that I labeled my dataset, but it was not ehough, so I need more autolabeled data.

### Week 3

## Conversation 5 (Date: 03/06/2024)

Lecturer: Marie

Questions for this conversation:

- [x] Question 1: How to improve my model for face detection? Can I use Bounding Box: Rotation, Shear, Brightness for the augmentation?
- [x] Question 2: How to make model for face recognition and what is the possible solutions for this?

This is the feedback on my questions.

- Feedback 1: Marie said my model is working well, I can add some more data, but it detects faces with a good accuracy. As for the augmentation, it can be dangerous for my model to use these settings, but you can try and check if it's good for your model
- Feedback 2: You can train one model and do you vs others, and then when a new user added, train this model again. I think that is the best option. The second option is to create each time a new model user vs others and compare them together to choose the best accuracy. But it's more difficult.  Marie also advised to use yolov8n(Nano) then yolov8s(Small) for better training time

## MVP02: working model (Date: 04/06/2024)

After the last feedback I completely retrained my model using a new dataset, so the accuracy was about 99% on the test, but for the video it was of course a bit lower, but still about 90% faces were captured. I also asked about how to make a face recognition model, we've talked with Marie and I said I will be busy doing it this week. I also showed that I can already add a new user to my database and that my Flask part is already done.

## MVP03: communication (Date: 11/06/2024)

I made my classification model and show my working program to Stijn, the model took a pictures of Stijn split it into train, test and val sets, then Stijn successfully logged in, and the welcome message printed on LCD Display in my box, he said that it would be nice to also print the name of the user on LCD Display, I said I was going to do it and also if the user is Teacher print Mr/Ms before name. My project is almost finished, so I just have to refactor some code and do deployment, so when I turn on my raspi it automatically opens a connection.