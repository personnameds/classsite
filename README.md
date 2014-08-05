classite v6

Homework
    -When teacher adds homework add docs and links at same time
    -admin shows related docs and links
    -Add Homework Due Date should be a multi-select widget
    -Make Class checkboxes prettier when adding homework
    -Should Assigned Work be part of homework_details rather than homework
    -RSS Feed
    
Documents
    -REDO BASED ON NEW HOMEWORK MODELS
    -Modify/Delete files shows path
    -Files need to delete if no longer used

Classlists
    -resize banner images when uploaded (saved link in readitlater)
    -banner image in admin is hardcoded so wont work but neat idea
    -staff members can choose to be on email list or not
    -minister of communication???
    
base.html
    -default banner hardcoded in, need to erase class banners for it to show
    
Day_No
    -Uses day version in kalendar, sure there is a better way but it works

Registration/Login
    -Login and Logout work but not checked
    -Registration commented out
    -Add class to registration
    -Do something like kidblog (code to add yourself)
    -Teachers can review and revise students passwords and logins
    -Teachers can change and edit their password
    
Schedule
    -look ahead?

Kalendar
    -Kalendar and Events work - old code
    -Kalendar change multiple days at once
    -KKSA and Class calendar????


Initialize
    -initialize is only for me
    -if fail security login redirect not setup
    -need to automate day creation based on schedule format, right now hardcoded
    
Schoolpage
    -modelform and views do I need that stuff

Homepage  

Overall
    -test.py
    -review and revise code
    -can other teachers edit other teacher messages on classpage and schoolpage
    -duplicate templates I do not need so many they are repetitive, just need to
     pass title as context variable
    -datefield.auto_now

classsite v5

Messages
    -edit messages????
    -if 0 messages topic should delete

Documents
    -different directories for each class

Contact

Homework
    -check if actually in class adding homework too
    -multiple class homework

Registration/Login
    -Change password works but can be done with less views and make it easier to do
    
Other
    -memcached
    -No hard coded urls (reverse)
    -Get_absolute_url
        -need to use and add so I can click from admin to see on website
    -feeds

    