# RideSafe 🚗
RideSafe is an all in one system that encourages safer driving through an incenitivizing leaderboard. We start off with a mobile app that runs on your phone that returns a dash cam photo to our server during your drive where we 

## Features
List the key features of your project.

- Mobil app that connects with our servers and webpage
- Backend with 2 servers running preprocessing, computing, our DBs, and hosting our webpage
- Webpage that displays current leaderboard with driving scores

## Installation ⬇️
1. Go to the webpage and create an account!
2. Download our APK off of this GitHub and install it on your iphone.


## Frontend 📱
Here are some photos of our frontend

![image](https://github.com/davisepalmer/RideSafe/assets/39246454/fbaa4ee7-1dbc-4cd3-af83-ef4edef32420)

![Screenshot 2](screenshots/screenshot2.png)

## Technologies Used ⚙️
Overall we used Python, Java, and Golang, but here is an exhaustive list of our the technologies we used:
- Android Studio using Java and XML with libraries: Google Map's API, Camera2 API, OKHTTP to send POST/GET Requests, and many other common helper libraries 
- From the app it sends photos through a POST to our webserver which decodes the image and runs it through an image detection and distance algorithm that calculates how far the next car is in front, and using many combined versions of data including accelerometer data, current speed limit, and a few other factors calculates a safety score and adds it to the user's profile driving
- From there you can access our webpage that displays a real-time leaderboard of the users with the highest scores 

## Road Map
We were really passionate about this project and talked about continuing it after the hackathon is over and we made a list of a few features and things we wanted to change/add in the future
1) Using the backcamera to analyze the driver's focus and changing his score based off of it
2) A more advanced algorithm for the score using more of the phone's sensors
3) Calibration of our distance algorithm, because we had only 27 hours for this project we couldn't get everything perfect, so this would be one of the first things we will do

## Contributors

- Owen Brown ([@owenmbrown](https://www.linkedin.com/in/owenbrown1/))
- Davis Palmer ([@Davis Palmer](https://www.linkedin.com/in/davisepalmer/))
- Harry Wu ([@Harry Wu](https://github.com/canuckiangamer))
- Marco Martinez ([@Marco Martinez](https://www.linkedin.com/in/marco-martinez-951672251/))


## License
No License

