import csv
import datetime as dt
from datetime import datetime
from statistics import mean, median, mode, stdev, median_low, median_high
import pandas as pd
from collections import Counter
from matplotlib import pyplot as plt
import numpy as np

path = "/Users/wsethapun20/Documents/Sleep/SurveyData4.csv"
file=open(path,newline='')
reader=csv.reader(file)

header=next(reader)

data=[]
for row in reader:
    # row = [Grade,Dorm,BedSchool,WakeSchool,BedWeekend,WakeWeekend,BedVac,WakeVac,ChangeStartSchool,ChangeAlarm,TimeGetReady,TimeDine,SleepQ,Sleepiness,Dozed,Concentration,Fatigue,Factor1,Factor2,Factor3,Factor4,Factor5]
    grade=int(row[0])
    dorm=row[1]
    if not row[2]:
        bedschool=row[2]
        wakeschool=row[3]
    else:
        bedschool=datetime.strptime(row[2],'%H:%M')
        wakeschool=datetime.strptime(row[3],'%H:%M')
    if not row[4]:
        bedweekend=row[4]
        wakeweekend=row[5]
    else:
        bedweekend=datetime.strptime(row[4],'%H:%M')
        wakeweekend=datetime.strptime(row[5],'%H:%M')
    if not row[6]:
        bedvac=row[6]
        wakevac=row[7]
    else:
        bedvac=datetime.strptime(row[6],'%H:%M')
        wakevac=datetime.strptime(row[7],'%H:%M')
    if not row[8]:
        changestart=row[8]
    else:
        changestart=datetime.strptime(row[8],'%H:%M')
    if not row[9]:
        changealarm=row[9]
    else:
        changealarm=datetime.strptime(row[9],'%H:%M')
    timegetready=row[10]
    timedine=row[11]
    sleepq=int(row[12])
    sleepiness=int(row[13])
    dozed=int(row[14])
    concentration=int(row[15])
    fatigue=int(row[16])
    factor1=row[17]
    factor2=row[18]
    factor3=row[19]
    factor4=row[20]
    factor5=row[21]
    data.append([grade,dorm,bedschool,wakeschool,bedweekend,wakeweekend,bedvac,wakevac,changestart,changealarm,timegetready,timedine,sleepq,sleepiness,dozed,concentration,fatigue,factor1,factor2,factor3,factor4,factor5])

def extractAllGradeBedWakeTime(n):
    times=[]
    for row in data:
        if not row[n]:
            continue
        else:
            if row[n]<datetime(1900,1,1,19,0,0):
                times.append(row[n]+dt.timedelta(1))
            else:
                times.append(row[n])
    return times

def extractEachGradeBedWakeTime(n,grade):
    times=[]
    for row in data:
        if row[0]!=grade:
            continue
        else:
            if not row[n]:
                continue
            else:
                if row[n]<datetime(1900,1,1,19,0,0):
                    times.append(row[n]+dt.timedelta(1))
                else:
                    times.append(row[n])
    return times

    
def plotStackedGradeBedWakeTime(n):
    plt.style.use('seaborn')    
    plt.xlabel('Time')
    plt.ylabel('Number of Students')
    grades=['M.1','M.2','M.3','M.4','M.5','M.6']
    eachGradeTime=[]
    grade=1
    while(grade<7):
        eachGradeTime.append(extractEachGradeBedWakeTime(n,grade))
        grade=grade+1
    if n==2 or n==4 or n==6:
        ran=(datetime(1900,1,1,21,0),datetime(1900,1,2,5,0))
        plt.hist(eachGradeTime,bins=8,range=ran,edgecolor='Black',stacked=True,label=grades)
        plt.axvline(median_high(extractAllGradeBedWakeTime(n)),color='red',label='median')
        plt.axvline(averageAllGradeTime(n),color='orange',label='mean')
        loc,lens=plt.xticks()
        plt.xticks(loc,('21', '22', '23', '24', '1','2','3','4','5'))
        plt.legend(loc="upper right")
        if n==2: plt.title('Bedtime of Students on School Nights')
        if n==4: plt.title('Bedtime of Students on Weekends')
        if n==6: plt.title('Bedtime of Students on Break')
    elif n==3 or n==5 or n==7:
        ran=(datetime(1900,1,2,4,0),datetime(1900,1,2,14,0))
        plt.hist(eachGradeTime,bins=10,range=ran,edgecolor='Black',stacked=True,label=grades) 
        plt.axvline(median_high(extractAllGradeBedWakeTime(n)),color='red',label='median')
        plt.axvline(averageAllGradeTime(n),color='orange',label='mean')
        loc,lens=plt.xticks()
        plt.xticks(loc,('4', '5', '6', '7', '8','9','10','11','12','13','14'))
        plt.legend(loc="upper right")
        if n==3: plt.title('Waketime of Students on School Nights')
        if n==5: plt.title('Waketime of Students on Weekends')
        if n==7: plt.title('Waketime of Students on Break')
    else:
        ran=(datetime(1900,1,2,4,0),datetime(1900,1,2,10,0))
        plt.hist(eachGradeTime,bins=12,range=ran,edgecolor='Black',stacked=True,label=grades) 
        plt.axvline(median_high(extractAllGradeBedWakeTime(n)),color='red',label='median')
        plt.axvline(averageAllGradeTime(n),color='orange',label='mean')
        loc,lens=plt.xticks()
        plt.xticks(loc,('4', '5', '6', '7', '8','9','10'))
        plt.legend(loc="upper right")
        if n==8: plt.title('Class Start Times Students Want')
        if n==9: plt.title('Waketime Students Want')
            
    plt.show()
    plt.savefig('Histogram Bed/Waketime.png')
    
def extractEachGradeSleepDuration(n,grade):
    durations=[]
    student=0
    while student<len(extractEachGradeBedWakeTime(n,grade)):
        duration=extractEachGradeBedWakeTime(n+1,grade)[student]-extractEachGradeBedWakeTime(n,grade)[student]
        duration=convert_timedelta(duration)
        durations.append(duration)
        student=student+1
    return durations

def extractAllGradeSleepDuration(n):
    durations=[]
    student=0
    while student<len(extractAllGradeBedWakeTime(n)):
        duration=extractAllGradeBedWakeTime(n+1)[student]-extractAllGradeBedWakeTime(n)[student]
        duration=convert_timedelta(duration)
        durations.append(duration)
        student=student+1
    return durations

def convert_timedelta(duration):
    seconds = duration.total_seconds()
    hours = seconds/3600
    return hours

def plotStackedGradeSleepDuration(n):
    plt.style.use('seaborn')    
    plt.xlabel('Sleep Duration')
    plt.ylabel('Number of Students')
    grades=['M.1','M.2','M.3','M.4','M.5','M.6']
    eachGradesTime=[]
    grade=1
    while(grade<7):
        eachGradesTime.append(extractEachGradeSleepDuration(n,grade))
        grade=grade+1
    ran=(3,13)
    plt.hist(eachGradesTime,bins=10,range=ran,edgecolor='Black',stacked=True,label=grades)
    plt.axvline(median_high(extractAllGradeSleepDuration(n)),color='red',label='median')
    plt.axvline(mean(extractAllGradeSleepDuration(n)),color='orange',label='mean')
    plt.legend(loc="upper left")
    if n==2: plt.title('Sleep Duration of Students on School Nights')
    if n==4: plt.title('Sleep Duration of Students on Weekends')
    if n==6: plt.title('Sleep Duration of Students on Break')
    plt.show()
    plt.savefig('Histogram Sleep Duration.png')
    
def extractEachGradeRelativeTime(n,grade):
    length=len(extractEachGradeBedWakeTime(n,grade))
    relativeTimes=[]
    student=0 
    if n==2 or n==4 or n==6:
        while student<length:
            relativeTime=extractEachGradeBedWakeTime(n,grade)[student]-datetime(1900,1,1,22,0)
            relativeTimes.append(relativeTime)
            student=student+1
    if n==3 or n==5 or n==7 or n==9:
        while student<length:
            relativeTime=extractEachGradeBedWakeTime(n,grade)[student]-datetime(1900,1,2,5,30)
            relativeTimes.append(relativeTime)
            student=student+1
    if n==8:
        while student<length:
            relativeTime=extractEachGradeBedWakeTime(n,grade)[student]-datetime(1900,1,2,8,0)
            relativeTimes.append(relativeTime)
            student=student+1
    return relativeTimes

def extractAllGradeRelativeTime(n):
    length=len(extractAllGradeBedWakeTime(n))
    relativeTimes=[]
    student=0 
    if n==2 or n==4 or n==6:
        while student<length:
            relativeTime=extractAllGradeBedWakeTime(n)[student]-datetime(1900,1,1,22,0)
            relativeTimes.append(relativeTime)
            student=student+1
    if n==3 or n==5 or n==7 or n==9:
        while student<length:
            relativeTime=extractAllGradeBedWakeTime(n)[student]-datetime(1900,1,2,5,30)
            relativeTimes.append(relativeTime)
            student=student+1
    if n==8:
        while student<length:
            relativeTime=extractAllGradeBedWakeTime(n)[student]-datetime(1900,1,2,8,0)
            relativeTimes.append(relativeTime)
            student=student+1
    return relativeTimes

def averageEachGradeTime(n,grade):
    timedeltas=extractEachGradeRelativeTime(n,grade)
    average_timedelta = sum(timedeltas, dt.timedelta(0)) / len(timedeltas)
    if n==2 or n==4 or n==6:
        baseTime=datetime(1900,1,1,22,0)
    if n==3 or n==5 or n==7 or n==9:
        baseTime=datetime(1900,1,2,5,30)
    if n==8:
        baseTime=datetime(1900,1,2,8,0)
    averageTime=baseTime+average_timedelta
    return averageTime

def averageAllGradeTime(n):
    timedeltas=extractAllGradeRelativeTime(n)
    average_timedelta = sum(timedeltas, dt.timedelta(0)) / len(timedeltas)
    if n==2 or n==4 or n==6:
        baseTime=datetime(1900,1,1,22,0)
    if n==3 or n==5 or n==7 or n==9:
        baseTime=datetime(1900,1,2,5,30)
    if n==8:
        baseTime=datetime(1900,1,2,8,0)
    averageTime=baseTime+average_timedelta
    return averageTime

def extractEachGradeRelativeHour(n,grade):
    relativeHour=[]
    for relativeTime in extractEachGradeRelativeTime(n,grade):
        relativeHour.append(convert_timedelta(relativeTime))
    return relativeHour

def plotGradevBedTime():
    x=[1,2,3,4,5,6]
    y2=[]
    y4=[]
    y6=[]
    y2error=[]
    y4error=[]
    y6error=[]
    i=1
    while(i<7):
        y2.append(mean(extractEachGradeRelativeHour(2,i)))
        y4.append(mean(extractEachGradeRelativeHour(4,i)))
        y6.append(mean(extractEachGradeRelativeHour(6,i)))
        y2error.append(stdev(extractEachGradeRelativeHour(2,i)))
        y4error.append(stdev(extractEachGradeRelativeHour(4,i)))
        y6error.append(stdev(extractEachGradeRelativeHour(6,i)))
        i=i+1
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.errorbar(x,y2,yerr=y4error,fmt='o',capsize=5,capthick=1,label='School')
    ax1.errorbar(x,y4,yerr=y2error,fmt='o',capsize=5,capthick=1,label='Weekend')
    ax1.errorbar(x,y6,yerr=y6error,fmt='o',capsize=5,capthick=1,label='Break')
    plt.legend(loc='upper left');
    plt.title('Average Bedtime Relative to 10PM')
    plt.style.use('seaborn')    
    plt.xlabel('Grade')
    plt.ylabel('Hours Relative')
    plt.show()
    plt.savefig('Scatter Grade and BedTime.png')
    
def plotGradevWakeTime():
    x=[1,2,3,4,5,6]
    y3=[]
    y5=[]
    y7=[]
    y9=[]    
    y3error=[]
    y5error=[]
    y7error=[]
    y9error=[]
    i=1
    while(i<7):
        y3.append(mean(extractEachGradeRelativeHour(3,i)))
        y5.append(mean(extractEachGradeRelativeHour(5,i)))
        y7.append(mean(extractEachGradeRelativeHour(7,i)))
        y9.append(mean(extractEachGradeRelativeHour(9,i)))
        y3error.append(stdev(extractEachGradeRelativeHour(3,i)))
        y5error.append(stdev(extractEachGradeRelativeHour(5,i)))
        y7error.append(stdev(extractEachGradeRelativeHour(7,i)))
        y9error.append(stdev(extractEachGradeRelativeHour(9,i)))
        i=i+1    
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.errorbar(x,y3,yerr=y3error,fmt='o',capsize=5,capthick=1,label='School')
    ax1.errorbar(x,y5,yerr=y5error,fmt='o',capsize=5,capthick=1,label='Weekend')
    ax1.errorbar(x,y7,yerr=y7error,fmt='o',capsize=5,capthick=1,label='Break')
    ax1.errorbar(x,y9,yerr=y9error,fmt='o',capsize=5,capthick=1,label='Student Choice')
    plt.legend(loc='upper left');
    plt.title('Average Waketime Relative to 5:30AM')
    plt.style.use('seaborn')    
    plt.xlabel('Grade')
    plt.ylabel('Hours Relative')
    plt.show()
    plt.savefig('Scatter Grade and WakeTime.png')
    
def plotGradevSchoolStart():
    x=[1,2,3,4,5,6]
    y8=[]
    y8error=[]
    i=1
    while(i<7):
        y8.append(mean(extractEachGradeRelativeHour(8,i)))
        y8error.append(stdev(extractEachGradeRelativeHour(8,i)))
        i=i+1
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.errorbar(x,y8,yerr=y8error,fmt='o',capsize=5,capthick=1)
    plt.title('Average Class Start Time Chosen by Students')
    plt.style.use('seaborn')    
    plt.xlabel('Grade')
    plt.ylabel('Hours Relative')
    plt.show()
    plt.savefig('Scatter Grade and Class Start Time.png')
    
def extractEachGradeRating(n,grade):
    rating=[0,0,0,0,0]
    for row in data:
        if row[0]==grade:
            if row[n]==0:
                rating[0]=rating[0]+1
            if row[n]==1:
                rating[1]=rating[1]+1
            if row[n]==2:
                rating[2]=rating[2]+1
            if row[n]==3:
                rating[3]=rating[3]+1
            if row[n]==4:
                rating[4]=rating[4]+1
    return rating

def extractAllGradeRatingList(n):
    rating=[]
    for row in data:
        rating.append(row[n])
    return rating

def extractEachGradeRatingList(n,grade):
    rating=[]
    for row in data:
        if row[0]==grade:
            rating.append(row[n])
    return rating

def plotGradevRating(n):
    x=[1,2,3,4,5,6]
    y=[]
    y2=[]
    yerror=[]
    i=1
    while(i<7):
        y.append(mean(extractEachGradeRatingList(n,i)))
        y2.append(median(extractEachGradeRatingList(n,i)))
        yerror.append(stdev(extractEachGradeRatingList(n,i)))
        i=i+1    
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.errorbar(x,y,yerr=yerror,fmt='o',capsize=5,capthick=1,label='mean')
    ax1.scatter(x,y2,label='median',color='red')
    plt.legend();
    plt.style.use('seaborn')    
    plt.xlabel('Grade')
    plt.ylabel('Rating')
    if n==12:
        plt.title('Sleep Quality Compared to Home')
    if n==13:
        plt.title('Sleepiness')
    if n==14:
        plt.title('Fell Asleep in Many Classes')
    if n==15:
        plt.title('Ability to Concentrate in Class')
    if n==16:
        plt.title('Fatigue')
    plt.show()
    plt.savefig('Scatter Grade and Effect of Sleep.png')
    

def plotRatings(n):
    x=[0,1,2,3,4]
    ax = plt.figure().add_subplot()
    bars1=extractEachGradeRating(n,1)
    bars2=extractEachGradeRating(n,2)
    bars3=extractEachGradeRating(n,3)
    bars4=extractEachGradeRating(n,4)
    bars5=extractEachGradeRating(n,5)
    bars6=extractEachGradeRating(n,6)
    ax.bar(x,bars1,label='1')
    ax.bar(x,bars2,bottom=bars1,label='2')
    bars = np.add(bars1,bars2).tolist()
    ax.bar(x,bars3,bottom=bars,label='3')
    bars = np.add(bars,bars3).tolist()
    ax.bar(x,bars4,bottom=bars,label='4')
    bars = np.add(bars,bars4).tolist()
    ax.bar(x,bars5,bottom=bars,label='5')
    bars = np.add(bars,bars5).tolist()
    ax.bar(x,bars6,bottom=bars,label='6')
    plt.style.use('seaborn')    
    plt.xlabel('Rating')
    plt.ylabel('Number of Students')
    plt.axvline(median_high(extractAllGradeRatingList(n)),color='red',label='median')
    plt.axvline(mean(extractAllGradeRatingList(n)),color='orange',label='mean')
    ax.legend()
    if n==12:
        plt.title('Sleep Quality Compared to Home')
    if n==13:
        plt.title('Sleepiness')
    if n==14:
        plt.title('Fell Asleep in Many Classes')
    if n==15:
        plt.title('Ability to Concentrate in Class')
    if n==16:
        plt.title('Fatigue')
    plt.show()
    plt.savefig('Bar Grade and Effect of Sleep.png')
    
def extractFactorList(n,grade):
    factorList=[]
    for row in data:
        if row[0]==grade or grade==7:
            factorList.append(row[n])
    return factorList
            
def extractFactorPointsEachRank(n,grade):
    cnt=Counter()
    for factor in extractFactorList(n,grade):
        if(n==17):
            cnt[factor]+=5
        if(n==18):
            cnt[factor]+=4
        if(n==19):
            cnt[factor]+=3
        if(n==20):
            cnt[factor]+=2
        if(n==21):
            cnt[factor]+=1
    return cnt

def plotFactor(grade):
    points=extractFactorPointsEachRank(17,grade)
    for i in [18,19,20,21]:
        points=points+extractFactorPointsEachRank(i,grade)
    factorNames=[]
    impact=[]
    for item in points.most_common(5):
        factorNames.append(item[0])
        impact.append(item[1])
    print(factorNames)
    print(impact)
    plt.bar(factorNames,impact)
    plt.style.use('seaborn')    
    plt.xlabel('Factor')
    plt.ylabel('Weighted Impact')
    if grade==7:
        plt.title('Comparison of Factors Affecting Sleep of All Students')
    else:
        plt.title('Comparison of Factors Affecting Sleep of M.'+grade+' Students')
    plt.show()
    plt.savefig('Bar Factor Affecting Sleep.png')
        
def getPlots():
    for i in [2,3,4,5,6,7,8,9]:
        plotStackedGradeBedWakeTime(i)
    for j in [2,4,6]:
        plotStackedGradeSleepDuration(j)
    plotGradevBedTime()
    plotGradevWakeTime()
    plotGradevSchoolStart()
    for k in [12,13,14,15,16]:
        plotRatings(k)
        plotGradevRating(k)
    for l in [1,2,3,4,5,6,7]:
        plotFactor(l)

getPlots()
