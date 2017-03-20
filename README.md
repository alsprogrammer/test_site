# Statistics-based knowledge assessment web application

Test web application for knowledge assestment.

## What is it?
This application is developed for use at educational organisations. The main idea is to determine whether a student passed the test using statistical approach. The application determines the threshold that can be passed by chance for the test student is passing. If the student overcomes that threshold the test is passed.
The test itself is defined as Microsoft .Net object written in C#. It is my legacy code and it takes a lot of time to rewrite it in Python :)

## Dependencies
The web part of the project is based on the [Flask](http://flask.pocoo.org/) framework.
As the project uses the legacy library written in C#, the project also uses the [Python for .NET](http://pythonnet.github.io/) project.

This work is published under <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.
