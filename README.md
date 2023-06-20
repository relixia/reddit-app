# reddit-app

This project is developed in 1 day as the second stage challange for an internship in Brandefense.

TR
Hedef: Reddit içerisindeki subredditler’de paylaşılan postların anlık olarak takip edilmesini sağlayan bir Python servisi geliştirmek. İsterlerimiz şunlar: Login olunabilmesi. Crawl edilen postların database’de tutulması. Postların anlık takip edilmesi. Postların API tarafından servis edilmesi. Yazılan tüm kodun test edilmesi. Dockerize edilmesi

ENG
Aim: Developing a Python service that provides instant tracking of posts on subreddits in Reddit. Requirements: login service, saving the crawled posts in an appropriate database. Instant tracking of the newly posted contents. Serving the posts via API calls. Testing. Dockerizing.

IMPORTANT!
To use the service, the user need to gather his account credentials in Reddit. Go to User Settings, and under Safety & Privacy tab, click Manage third-party app authorization link. For the rest, here is a step-by-step demonstration:
![Screen-Shot-2018-02-28-at-5 37 01-PM-e1520217895757-1200x649](https://github.com/relixia/reddit-app/assets/77904399/90732d8f-595d-4d5d-979b-572cab86bd5e)

![Screen-Shot-2018-02-28-at-6 55 38-PM-1200x376](https://github.com/relixia/reddit-app/assets/77904399/2f4170fd-1704-4123-8a69-3fed329cac74)

<img width="903" alt="Screen-Shot-2018-02-28-at-7 02 45-PM" src="https://github.com/relixia/reddit-app/assets/77904399/869e6045-3b68-4228-9892-9d16eedf317f">



The 14 chars information will be the Client ID, and the 27 chars will be the Client Secret. For the User Agent, you can just enter "deneme" without quotes. 
Then, the user can write the name of the subreddit that will be tracked. There is no lower or upper limit for the number of subreddits, and all of them will be tracked simultaneously. To see if the service is working properly without waiting for a new post in a subreddit, the last 10 posts of the subreddit also will be saved in the database. Then, the service checks in every 60 seconds to see if there is a new post or not.
As the database, sqlite3 is used. 

While the program is working, everything can be seen from the database easily. Here is an example run:
<img width="1470" alt="Ekran Resmi 2023-06-20 08 02 48" src="https://github.com/relixia/reddit-app/assets/77904399/a2df7ec6-0079-4e15-9bd5-732b782f4334">

Here is the subreddits at when the screenshot of the above image is taken:
<img width="1470" alt="Ekran Resmi 2023-06-20 08 03 13" src="https://github.com/relixia/reddit-app/assets/77904399/1201419c-c003-4c50-bbfe-47dd4422611f">

(In the database picture there is another post seen with the title "54 years after the..." after the one with title "Mass Effect..." but it is not visible here since I forgot to refresh the subreddit page)
<img width="1470" alt="Ekran Resmi 2023-06-20 08 03 21" src="https://github.com/relixia/reddit-app/assets/77904399/d0c064ba-61b1-4578-a742-03180915ee05">

Here is the screenshot of http://localhost:5000/posts 
<img width="1470" alt="Ekran Resmi 2023-06-20 08 00 34" src="https://github.com/relixia/reddit-app/assets/77904399/a66a6406-8a4b-4371-8ead-880f60d55cda">


If you face with any problem, feel free to contact: 
bugra-net@hotmail.com

Buğra Çayır

