# commentbot
A YouTube comment bot to comment using multiple google accounts on one video.

**WARNING: I am not responsible for anyone using this code to violate YouTube's Terms of Service.**

Requirements:
`pip install selenium`

This program uses a hack to bypass Google's automation detection and login to many Google accounts sequentially.

Intended for use by people with many Google accounts who want to leave a comments on a single YouTube video with many accounts (e.g. realistic comment botting).

Works (on my Windows device) for at least Chrome version 128.0.6613.113 on 30/08/2024.

**TO USE:**
Insert comments to be left on video to COMMENTS list on line 87 as strings.
Insert usernames and passwords into CREDENTIALS dict on line 95 in the form "email": "password".
Put the URL of the YouTube video to be commented on into the URL variable on line 103 inside the speech marks.

**RESULT:**
The YouTube video at the specified URL will receive, one by one, a comment randomly selected from the COMMENTS list, from each Google account in the order they appear in the CREDENTIALS dictionary.
When all the comments have been left, the chromedriver will close.

**NOTE:**
This code is entirely reliant on the flow of the UI. If Google changes even the tiniest bit of the program flow (e.g. Google changes the name of the "Next" button to "Continue"), this code will almost certainly break, as it is "blind", and just follows a predefined set of instructions.

However, if a page does not load in time, in most cases the program tries to look for the next element, and if it cannot find it then it waits another 2 seconds before looking again. This is to stop the program breaking if a page takes unusually long to load. However if it cannot find the element after 10 tries, it gives up and the program terminates.
