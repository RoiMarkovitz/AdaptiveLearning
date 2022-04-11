# Adaptive Learning of arithmetic for third grades - Final project in computer science degree

The project examines the potential of teaching arithmetic in Israel using an adaptive learning method.

We examined data and publications about students' achievements in mathematics and reading comprehension in Israel. We have learned that achievements are at a low and steady decline, even compared to other countries.

We have concluded that the low achievements are directly because the manner of transferring and teaching the material in the schools has not changed over the years, but the students and the technology have indeed changed. Today's students belong to the alpha generation and therefore the mode of teaching should be updated accordingly.

We conducted an in-depth literature review around the topic of adaptive learning. Following the review, we decided to incorporate key elements of adaptive learning in the project. These elements include performing micro-level intervention and managing precise profiles of learners (maintaining levels and percentages of adaptation to learning styles, dividing exercises into categories, etc.). Since the target audience of the project are children in third grade, we decided to incorporate elements of gamification as well.

After reviewing the literature, we conducted a market survey. We surveyed five competitors from Israel and around the world. We have concluded that the competing systems lack key elements of adaptive learning and that today there is no system in the Hebrew language for adaptive learning of arithmetic and reading comprehension in Israel.

Next, we performed a detailed design of the adaptive learning system we developed. We decided to include four main algorithms: the first is the "examinator". This algorithm is responsible for managing a learning styles questionnaire and a level quiz that will be presented to a new learner in the system. The second is the "learner profile". This algorithm is responsible for analyzing the results of the questionnaire, the quiz, and the ongoing learner activity in the system. The third is the "tutor". This algorithm is responsible for communicating with the learner and determining the learning style in which the exercises will be presented. The fourth is the "expert". This algorithm is responsible for composing the set of exercises most appropriate for the learner level. In addition, we included five elements of gamification: a scoring system, constructive feedback in real time, a response time frame, splitting the material into small units and the principle of gradation.

After that we moved on to the system development phase. The resulting product is a POC for an adaptive learning system of third-grade arithmetic. The product is written using the Python programming language interfacing with MongoDB database.

In the next step, we performed an evaluation of the project. We conducted an experiment with the participation of 11 third graders who used our system and the system of one of the competitors we reviewed. The results of the experiment are that there is a gap of 10.6% in the success of the participators in favor of using the system we developed. In addition, there are gaps of 18.18% to 23.64% in the user experience in favor of using the system we developed. The results show that we met the indices set at the beginning of the project.

The results of the experiment are a sign for the success of the POC, they have strengthened in us the insight that there is significant potential in teaching arithmetic in Israel using the adaptive learning method.

The development phase of the POC took about two weeks. 

[Click to view the full final project report](/documentation/Final%20Project%20Report.pdf)

https://user-images.githubusercontent.com/68189545/162814470-1cda5caa-f0b9-472d-86bc-d7afb3a1422d.mp4


### Guidelines for running the program 

1. **MongoDB Community Server** 
     - https://www.mongodb.com/try/download/community

2. **Python**
     - https://www.geeksforgeeks.org/how-to-install-python-on-windows

3. **Python Libraries**
     - The following commands should be written in the terminal:
      ```
      python -m pip install Pillow
      python -m pip install pygame
      python -m pip install pymongo
      ```
       
4. **Run main.py** 
     - Open the terminal in the project's root directory and write the command: 
      ```
      python main.py
      ```  
      
5. **Have Fun**






 

 
