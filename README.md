# Workout

This is an application designed in Python to host my workout regimen. 

It is an implementation of
nSuns 5/3/1 split. More specifically, it is an implementation of the 6 Day program, which can be found [here](https://drive.google.com/file/d/0B8EbfzFB0mBrSTZrX2E1d3hHNk0/view "nSuns 5321 LP 6 Day").

For obvious reasons, the phone number you text to use this program is private. Ask Ben for the phone number if you wish to use the program. 

## Summary
* Easy to understand and simple registration process.
* Always online, accessible 24/7.
* Users can warmup, workout, and deload all in one place.
* Allows for dynamic customization of user lifts.
* An unlimited number of users can have their own profiles. 

## Usage

These are the main functions of the program. The below guide can also be seen at https://pastebin.com/BNcZ8yYZ.

### "warmup"
This is the first function you will probably use every workout. This function will return three sets of a particular exercise (today's main lift, to be specific) that are 40%, 50%, and 60% of that lifts training max. 


### "workout"
This is the next function you will use in most cases, and is the main function of this program. This function operates differently depending on the day. If it's a Monday or Saturday, it will return a large text with the complete remainder of the workout. This text functions identically to the warmup function (albeit with more complicated math behind the hood), so you can just do the listed sets and move on with your life. On the other hand, if it is Tuesday, Wednesday, Thursday, or Friday, this will return your "5/3/1" split. The idea behind this is pretty simple to understand. You are sent three sets: a set of five reps, a set of three reps, and a set of "one plus" reps. The "1+" is your AMRAP (As Many Reps As Possible) set and just means that you want to do as many reps as possible. The amount of reps you do here is important and is used by the next function I'll describe. 


### "(# of reps) reps"
This is a more simple to understand function that just takes the amount of reps you did during your during your AMRAP set and uses that to update today's lift's training max. For example, if today is a bench press day and you did 4 reps during the AMRAP set, you would send the message "4 reps." The amount of reps you do determines how much the training max increases. 0-1 reps will result in a 0 lb increase, 2-3 will result in a 5 lb increase, 4-5 will result in a 10 lb increase, and anything above 5 reps yields a 15 lb increase. After your training max is updated, you are given a list of sets to do, similarly to the warmup function. 

### "deload (# decrease) (workout)"
Occasionally, you will be unable to do the amount of reps asked by the program. It is up to your discretion what you wish to do in the event this occurs, but should you wish to lower the weight of what the program is asking for you can use this function. The syntax of this function is shown above. For example, to lower your deadlift training max by 10 lbs, you would send "deload 10 deadlift." After your training max is lowered, the program sends an updated version of today's workout with the lowered values.


### "maxes"
From here, the functions fortunately get much simpler to describe. When you initially registered your lifts, the values you gave were stored for comparison. At any time, you can call this function and will be given statistics showing where you are now versus when you first started using this program.


### "undo"
Self explanatory. Undoes the last change to your stored values. For example, if you just increased your overhead press training max by 10 lbs instead of 5 lbs, you can send this message to revert everything back to the way it was before you increased anything. This can only revert the most RECENT change; anything beyond that is unrecoverable.