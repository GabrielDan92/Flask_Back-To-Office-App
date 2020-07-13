#### The fully functional website is currently hosted on Python Anywhere's platform, and can be found <a href="http://gabrieldan.pythonanywhere.com/">here</a>.
<p>
  
## Why did I built this app? 
  Once the Covid-19 lockdown around the world eases (hopefully sooner than later), some of you will be in charge of gradually bringing the staff back into the office. But how do you keep track of everyone coming to work and if the maximum number of colleagues in the office for a given day has been reached? I believe that there is an easier way to centralize and keep track of every staff member that will come to the office then just counting email requests from colleagues or try to use a shared Office solution. <p>
  By all means, you could try to use shared Excel workbooks saved on shared drives, OneDrive, SharePoint or even use Excel Online as an alternative, but only the ones who've used these solutions know what hassle it is to have a large number of users using the same file at the same time. From users editing the same cell, locked out users while the file is in use, corrupted or missing data, to users hiding or moving columns, formulas, there are a lot of things that can go wrong. <p>
And that's how the Back-To-Office App came into existence. :) <p>
  
## How did I built the app and what tools did I use?
* Flask
  * Template inheritance
  * Authentication: altough I spend a lot of time on Stack Overflow when I encountered a blocking point and I found great resources throughout the development phase, I must give credit where credit is due: Anthony Herbert's tutorial on  <a href="https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login">implementing authentication to Flask apps</a> was awesome and I can't recommend it highly enough.
  * a lot of values being sent from the Back-End to the Front-End passed through ```<render_template>``` as arguments
  * and many queries to the db
* HTML, CSS, javaScript for the Front-End
* jQuery AJAX for ```POST``` requests
* Bootstrap for almost all styling properties
* W3.CSS for the employee tables
