# API REFERENCES
Note: The format using to send data from server to client and backwards is JSON and HTTP protocol is used

## User
---
#### *POST api/v1/accounts/*
Create new user account

Parameters: username, email, password, confirm_password, first_name

---
#### *POST api/v1/auth/login/*
User login

Parameters: username, password

---
#### *POST api/v1/auth/logout/*
User logout

---
#### *GET api/v1/accounts/*
Get all user info from server

---
#### *GET api/v1/auth/accounts/:username/*
Get specific user info from server

---
#### *PUT api/v1/auth/accounts/:username/*
Update user profile

Parameters: user, password, email

---
#### *GET api/v1/account/avatar/:username/*
Get the avatar of a user

JSON format
```
{
  "avatar": "static/img/default.jpg"
}
```

---
#### *POST api/v1/account/follow/*
Follow a user

JSON format
```
{
  "id": 1,
  "username": "admin",
  "facebook_id": "123456789"
}
```

---
#### *POST api/v1/account/unfollow/*
Unfollow a user

JSON format
```
{
  "id": 2,
  "username": "user",
  "facebook_id": "987654321"
}
```

---
## Topic
---
#### *GET api/v1/topics/*
Get all topics available

JSON format
```
{
  {
    "id": 1,
    "name": "General"
    "description": "test"
  },
  {
    "id": 2,
    "name": "Technology",
    "description": "test"
  }
}
```

---
#### *GET api/v1/topic/:topicID/*
Get the topic with id specified

JSON format
```
{
  "id": 1,
  "name": "General",
  "description": ""
}
```
---
#### *GET api/v1/topics/?keyword=test*
Get 10 most related topics with the keyword provided

---
#### *POST api/v1/topic/*
Add new topic to server

JSON format
```
{
  "name": "Test",
  "description": "Test"
}
```
---
## Question
---
#### *GET api/v1/questions/?keyword=test*
Get 10 most related questions with the keyword provided
 
JSON format
```
{
  {
    "id": 1,
	"question": "Test"
  },
  {
	"id": 2,
	"question": "Sample"
  }
}
```
---
#### *GET api/v1/question/?questionID=1*
Get the question with the id provided

JSON format
```
{
  "id": 1,
  "question": "Test"
}
```
---
#### *GET api/v1/question/topic/?questionID=1*
Get all topics for the question with id specified

---
#### *GET api/v1/topic/question/?topicID=1&startID=1&count=10*
Get 'count' newest questions from startID downwards which belongs to the topic with id specified

If startID equals 0, get from newest questions

---
#### *POST api/v1/question/*
Post new question to server

JSON format
```
{
  "question": "Test",
  "content": "Test",
  "topics": "1|2|3"
}
```

---
#### *POST api/v1/question/topic/?questionID=1*
Add new topic for the question with id specified

JSON format
```
{
  "id": 4,
  "name": "Music",
  "description": ""
}
```

---
#### *PUT api/v1/question/?questionID=1*
Update a question with id specified

JSON format
```
{
  "question": "Test",
  "content": "Test"
}
```

---
#### *DELETE api/v1/question/topic/?questionID=1*
Delete topic for the question with id specified

JSON format
```
{
  "id": 1,
  "name": "General",
  "description": ""
}
```

---
## Answer
---
#### *GET api/v1/answers/?questionID=1*
Get all answer of a question with id specified

---
#### *GET api/v1/answers/?questionID=1&startID=1&count=10*
Get 'count' answers for a question with id specified, from startID (sorted by created_date)

---
#### *POST api/v1/answer/?questionID=1*
Post an answer for a question with id specified

JSON format
```
{
  "content": "Test"
}
```

---
#### *PUT api/v1/answer/?answerID=1*
Update an answer with id specified

JSON format
```
{  
  "content": "Test"
}
```

---
## Comment
---
#### *GET api/v1/comments/?id=1*
Get all comments for a post (question or answer) with id specified

---
#### *POST api/v1/comment/?id=1*
Post new comment for a post (question or answer) with id specified

---
#### *PUT api/v1/comment/?commentID=1*
Update a comment with id specified

