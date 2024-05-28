# FaceAuth - Project One

**FIRST & LAST NAME:** Mykyta Tsykunov

**Sparring Partner:** Danylo Bordunov

**Project Summary in max 10 words:** Face authentication program allows users to login the study platform

**Project Title:** FaceAuth

---
### Week 01
First of all, I have consultation with **Marie**, where we have discussed my plan for training my AI model, she said that I could try to make the face detecton model first, get accuracy above 90% and then start my face recognition.

Second of all, I spoke to **Frederik**, we have discussed how my database would look like and how to connect to it, he said he will send me some guides on how to implement mySQL database in python.

Third of all, I was talking with **Tijn** about my maker part, where I will use some plywood and apply laser cutting on it, I made another consultation, because I want some help to make a pdf file for laser cutting, so I can come and cut the pieces of my box.

Working on dataset, preparing data and label it, I tried to train my AI model several times, but the accuracy is not good.

---
### Week 02

I have talked to **Tijn**, he was helping with creating a box for my rapsi, I start working in illustrator to create a nice layout, then I will send it to Deepnest.io to save space and materials.

Then I have an a consultation with **Christophe**, my idea was to create some sort of web service, but it turned out to be a very difficult task for the first project. Because I wanted to use a webapp, MySQL database, my AI model and raspi all at once. Christophe advised to create some separate scripts, for instance: I run the script signup.py to sign up and save the user to the database, then run script for recording user's face and train face recognition model. And last but not least I run my app.py, connect to my raspi and do face authentication, if the authentication ends up successfully, It will show a welcome message on an LCD Display. The problem is I wanted all these "actions" to be in my webapp, so I needed some web service to connect to my model and send some images(don't forget that we need talk to raspi from this web service as well), and that is the topic of the 2nd year of MCT CT&AI. He sent me an example of Flask website, I'm going to use it to create a simple form page, where you can sign up and your data will be saved in MySQL database.
