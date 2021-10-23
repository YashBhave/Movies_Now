# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 09:19:03 2021

@author: HP
"""

import streamlit as st
import pandas as pd
import numpy as np
#import math
#from apyori import apriori


#HEADER OF THE PAGE
st.title("Watch NOW")
st.image('Watch_Now.png',width=100) #LOGO
st.subheader('One click away') #Tagline
st.text("This is a platform where you can keep a tab on your daily series and movie status.") #Description



#Loading profile data into python from database
User_Profiles = pd.read_excel('Movies_Now_Database.xlsx', 'Profile',usecols=['First Name','Last Name','Username','Password','Mobile Number','Genre Preference'])


#Login Code for profile username and password
Login_Hide=0
UserName = st.text_input('Enter Username')
Password = st.text_input('Enter Password',type="password")

#If login is entered
if (Login_Hide==0):
    #Checking Credentials from database
    InputCheck=[]
    InputCheck= np.where(((User_Profiles["Username"]==UserName) & (User_Profiles["Password"]==Password)),User_Profiles["Username"],None)
    InputCheck= list(filter(None,InputCheck))   

#If the credentials is correct it will check if the userdata list is populated with correct username from database (Unique for a user)
if len(InputCheck)>0:
    Login_Hide=1
    #Data loading for the logged in user
    Episode_Data=pd.read_excel('Movies_Now_Database.xlsx',"Episode Data",usecols=['Series Id','Series name','Season','Episode No','Episode Name','Episodes Aired date','Aired (1 or 0)','Run Time (minutes)'])
    UserStatsData = pd.read_excel('Movies_Now_Database.xlsx',"Profile Episode Map")
    UserSeriesMap = pd.read_excel('Movies_Now_Database.xlsx',"Profile Series Map 2")
    Series_Data=pd.read_excel('Movies_Now_Database.xlsx', 'TV Series',usecols=['Series Id (PK)','Name','Release Date','Number of Seasons','Number of Episodes','Total Time (min)','Genre1','Genre2','Genre3','Star Cast 1','Star Cast 2','Star Cast 3','IMDB','Language1','Language2','Platform','Image link'])
    user_data = pd.read_excel('Movies_Now_Database.xlsx',sheet_name = "Profile Series Map")
    
    
    #HOMEPAGE CODE
    #Selected User Data for profile
    #First name data of user
    First_Name = np.where(User_Profiles["Username"]==UserName,User_Profiles["First Name"],None)
    First_Name= list(filter(None,First_Name))
    #Last name data of user
    Last_Name = np.where(User_Profiles["Username"]==UserName,User_Profiles["Last Name"],None)
    Last_Name= list(filter(None,Last_Name))
    #Genre preference data of user
    Genre_Preference = np.where(User_Profiles["Username"]==UserName,User_Profiles["Genre Preference"],None)
    Genre_Preference= list(filter(None,Genre_Preference))
    
    #Welcoming Users Message
    st.text("Welcome - "+ First_Name[0] + " " + Last_Name[0])

   #Showing Users Genre Preference
    st.text("Genre Preference- "+ Genre_Preference[0])
    st.image('watchnow_pic.jpg')

    #User to switch between sections for the application
    PageSelection = st.radio("Select Page ", ('Search Page','Recommendations' ,'User Stat'))


    




    #SEARCH PAGE CODE
    #Based on radion button selection checking if it is search page
    if PageSelection=="Search Page":
        #Header of serach page with tagline
        st.title('Search here')
        st.text('Start bingeing now!')
        
        #Filters for the search page
        GenreFilter=st.selectbox("Select a genre...",['Genre','Thriller','Crime','Comedy','Romance','Fantasy'], index=0)
        LanguageFilter=st.selectbox("Select a language...",['Language','Hindi','English','Bengali','Marathi','German','Others'], index=0)
        IMDBRatingFilter=st.slider("IMDB Rating",min_value=int(Series_Data['IMDB'].min()),max_value=int(Series_Data['IMDB'].max()),step=1,value=int(Series_Data['IMDB'].min()))
        
        #Initializing filter search lists                 
        Filtered_Series_Name=[]
        Filtered_Series_Name1=[]
        Filtered_Series_Name2=[]
        Filtered_Series_Name3=[]
        Filtered_Series_Name4=[]    
        Series_Name=""
        
        #Initializing with all the series names
        Filtered_Series_Name = list(Series_Data["Name"])
        
        #Filtered series name based on genre
        if GenreFilter!="Genre":
            Filtered_Series_Name4=np.where(((Series_Data["Genre1"]==GenreFilter) | (Series_Data["Genre2"]==GenreFilter) | (Series_Data["Genre3"]==GenreFilter)),Series_Data["Name"],None)
            Filtered_Series_Name4= list(filter(None,Filtered_Series_Name4))

        #Filtered series name based on language
        if LanguageFilter!="Language":
            Filtered_Series_Name2= list(np.where(((Series_Data["Language1"]==LanguageFilter) |(Series_Data["Language2"]==LanguageFilter)),Series_Data["Name"],None))
            Filtered_Series_Name2= list(filter(None,Filtered_Series_Name2))
        
        #Filtered series name based on IMDB Rating
        if IMDBRatingFilter!=0:
            Filtered_Series_Name3=list(np.where((Series_Data["IMDB"]>IMDBRatingFilter),Series_Data["Name"],None))
            Filtered_Series_Name3= list(filter(None,Filtered_Series_Name3))
        
        #Intersection of all filtered lists
        if len(Filtered_Series_Name2)>0 or LanguageFilter!="Language":
            Filtered_Series_Name=list(set(Filtered_Series_Name) & set(Filtered_Series_Name2))
        if len(Filtered_Series_Name3)>0 or IMDBRatingFilter!=0:
            Filtered_Series_Name=list(set(Filtered_Series_Name) & set(Filtered_Series_Name3))
        if len(Filtered_Series_Name4)>0 or GenreFilter!="Genre":
            Filtered_Series_Name=list(set(Filtered_Series_Name) & set(Filtered_Series_Name4))
        
        #Result display for loop
        Series_Selected=''
        #Checking conditions if any 1 filter is selected and Filters selected have a value to display
        if len(Filtered_Series_Name)>0 and (LanguageFilter!="Language" or (IMDBRatingFilter!=0 and IMDBRatingFilter!=int(Series_Data['IMDB'].min())) or GenreFilter!="Genre"):
            listcheck=[]
            for i in range(0,(len(Filtered_Series_Name))):
                if Filtered_Series_Name[i] not in listcheck:
                    listcheck.append(Filtered_Series_Name[i])
                    Series_Image=np.where(((Series_Data["Name"]==Filtered_Series_Name[i])),Series_Data["Image link"],None)
                    Series_Image= list(filter(None,Series_Image))
                    st.image(Series_Image[0],width=200)
                    
                    st.text(Filtered_Series_Name[i])
                    
            #Link to episode section dropdown of selected series
            Series_Selected=st.selectbox("Select a series...",listcheck, index=0)
        
        #If no filters are selected
        else:
            st.text("No Series Available with current filters")
        
        
        
        
        
        
        
        
        #EPISODE DATA SECTION   
        if Series_Selected!='':
            
            #Initializing selected series data  (Aired date, run time, IMDB rating, genre, Starcast etc.)
            DateList = np.where(Episode_Data['Series name']==Series_Selected,Episode_Data["Episodes Aired date"],None)
            DateList= list(filter(None,DateList))
            RunTime=np.where(Series_Data["Name"]==Series_Selected,Series_Data["Total Time (min)"],None)
            RunTime= list(filter(None,RunTime))
            IMDB_rating=np.where(Series_Data["Name"]==Series_Selected,Series_Data["IMDB"],None)
            IMDB_rating= list(filter(None,IMDB_rating))
            Series_Image = np.where(Series_Data['Name']==Series_Selected,Series_Data["Image link"],None)
            Series_Image= list(filter(None,Series_Image))
            Series_Genre1 = np.where(Series_Data['Name']==Series_Selected,Series_Data["Genre1"],None)
            Series_Genre1= list(filter(None,Series_Genre1))
            Series_Genre2 = np.where(Series_Data['Name']==Series_Selected,Series_Data["Genre2"],None)
            Series_Genre2= list(filter(None,Series_Genre2))
            Series_Genre3 = np.where(Series_Data['Name']==Series_Selected,Series_Data["Genre3"],None)
            Series_Genre3= list(filter(None,Series_Genre3))
            Series_StarCast1 = np.where(Series_Data['Name']==Series_Selected,Series_Data["Star Cast 1"],None)
            Series_StarCast1= list(filter(None,Series_StarCast1))
            Series_StarCast2 = np.where(Series_Data['Name']==Series_Selected,Series_Data["Star Cast 2"],None)
            Series_StarCast2= list(filter(None,Series_StarCast2))
            Series_StarCast3 = np.where(Series_Data['Name']==Series_Selected,Series_Data["Star Cast 3"],None)
            Series_StarCast3= list(filter(None,Series_StarCast3))
                        
            #Series details (Name, IMDB Rating, run time, date released, Image)
            st.title(Series_Selected)
            st.text('TV Series- Released on '+ DateList[0] + ' Total Run Time-' + str(RunTime[0]) +' minutes' )
            st.text("⭐ "+str(IMDB_rating[0])+ " /10")
            st.image(Series_Image[0], width=200)
            st.text(str(Series_Genre1[0])+", "+str(Series_Genre2[0])+", "+str(Series_Genre3[0]))
            st.text(str(Series_StarCast1[0])+", "+str(Series_StarCast2[0])+", "+str(Series_StarCast3[0]))
            
            
            #Dropdown of seasons of the series selected
            Season_Count = np.where(Series_Data['Name']==Series_Selected,Series_Data["Number of Seasons"],None)
            Season_Count= list(filter(None,Season_Count))
            SeasonNumberList=[]
            for i in range(1,(int(Season_Count[0])+1)):
                SeasonNumberList.append(str(i))
            
            #Dropdown for season selection
            SeasonFilter = st.selectbox(
            'Season',
            SeasonNumberList)
            
            #Episode list filtered based on selected season
            Episodes_List = np.where(((Episode_Data['Series name']==Series_Selected) & (Episode_Data['Season']==int(SeasonFilter))),Episode_Data["Episode Name"],None)
            Episodes_List= list(filter(None,Episodes_List))
            
            #populating on display filtered episode names
            for i in Episodes_List:
                st.text(i)
                
        #If no series is selected
        else:
            st.text("Please Select Series")
    
    
    
    
    
    
    
    #USER STAT PAGE
    #Based on radio button selection displaying this page
    elif PageSelection=="User Stat":
        #Heading of the user stat page
        st.title('User Stats')
        st.text('Check out your stats')
        
        #Logged in users watched TV series and episodes
        UserSeriesData = np.where(UserStatsData['Username']==UserName,UserStatsData["SeriesName"],None)
        UserSeriesData= list(filter(None,UserSeriesData))
        UserEpisodeData = np.where(UserStatsData['Username']==UserName,UserStatsData["Episode Name"],None)
        UserEpisodeData= list(filter(None,UserEpisodeData))  
        
        #Episode run time of the watched episodes of user who has logged in
        UserEpisodeTime=[]
        for i in range (1,(int(len(UserSeriesData)))):
            UserEpisodeTime = UserEpisodeTime + list(np.where(((Episode_Data['Series name']==UserSeriesData[i]) & (Episode_Data['Episode Name']==UserEpisodeData[i])),Episode_Data["Run Time (minutes)"],None))
            UserEpisodeTime= list(filter(None,UserEpisodeTime))
        
        #Checking total time spent by user watching episodes based on mapping (Hours and minutes)
        #TotalTimeSpent = 0
        #for i in UserEpisodeTime:
         #   TotalTimeSpent = TotalTimeSpent + int(i)
          #  Total_Hours= math.floor(TotalTimeSpent/60)
          #  Total_Mins=TotalTimeSpent - (Total_Hours*60)
          #  if Total_Mins<0:
           #     Total_Mins=0
        
        #Displayng run time to user he has spent
       # st.text("Series Watch Time - " + str(Total_Hours) + " Hours " + str(Total_Mins) + " Minutes")
       # TotalSeriesWatched = list(dict.fromkeys(UserSeriesData))
       # st.text("Total Series Watched- " +str(len(TotalSeriesWatched)))
        
        #Displaying count of series user has watched        
        SeriesWatched = np.where(UserSeriesMap['Username']==UserName,UserSeriesMap["Series Name"],None)
        SeriesWatched= list(filter(None,SeriesWatched))
        
        #Displaying count of genres he has watched
        UserGenreData=[]
        for i in SeriesWatched:
            UserGenreData= UserGenreData+ list(np.where(Series_Data['Name']==i,Series_Data["Genre1"],None))
        UserGenreData= list(filter(None,UserGenreData))
        st.header("Genres Watched")
        st.text("Action-" +str(UserGenreData.count("Action")))
        st.text("Thriller-" + str(UserGenreData.count("Thriller")))
        st.text("Drama- " + str(UserGenreData.count("Drama")))
        st.text("Comedy- " + str(UserGenreData.count("Comedy")))
        st.text("Suspense- " + str(UserGenreData.count("Suspense")))
        st.text("Animation- " + str(UserGenreData.count("Animation")))
        st.text("Crime- " + str(UserGenreData.count("Crime")))
        st.text("Documentary- " + str(UserGenreData.count("Documentary")))
        st.text("Fantasy- " + str(UserGenreData.count("Fantasy")))
        
                
        
        
        
        
    #RECOMMENDATIONS PAGE
    #Displaying recommendations page based on selection
    elif PageSelection=="Recommendations":
        #Recommendations page title and text
        st.title('Recommendations')
        st.text('Personalized for you')
        
        #Filtering the user watched series
        SeriesWatched = np.where(UserSeriesMap['Username']==UserName,UserSeriesMap["Series Name"],None)
        SeriesWatched= list(filter(None,SeriesWatched))
        
        #Checking the first genre of the watched series
        UserGenreData=[]
        SeriesWatchedImage=[]
        for i in SeriesWatched:
            UserGenreData= UserGenreData + list(np.where(Series_Data['Name']==i,Series_Data["Genre1"],None))
            SeriesWatchedImage = SeriesWatchedImage + list(np.where(Series_Data['Name']==i,Series_Data["Image link"],None))
        
        #filtering out null from genres
        SeriesWatchedImage= list(filter(None,SeriesWatchedImage))
        UserGenreData= list(filter(None,UserGenreData))
        #UserGenreData = [x for x in UserGenreData if str(x) != 'nan']
        
        #Based on genres watched searching other TV series having same genres in all 3 columns
        RecommendedSeriesName=[]
        RecommendedSeriesImage=[]
        for i in UserGenreData:
            RecommendedSeriesName=RecommendedSeriesName+ list(np.where(((Series_Data["Genre1"]==i)),Series_Data["Name"],None))
            RecommendedSeriesName=RecommendedSeriesName+ list(np.where(((Series_Data["Genre2"]==i)),Series_Data["Name"],None))
            RecommendedSeriesName=RecommendedSeriesName+ list(np.where(((Series_Data["Genre3"]==i)),Series_Data["Name"],None))
            
            RecommendedSeriesImage=RecommendedSeriesImage+ list(np.where(((Series_Data["Genre1"]==i)),Series_Data["Image link"],None))
            RecommendedSeriesImage=RecommendedSeriesImage+ list(np.where(((Series_Data["Genre2"]==i)),Series_Data["Image link"],None))
            RecommendedSeriesImage=RecommendedSeriesImage+ list(np.where(((Series_Data["Genre3"]==i)),Series_Data["Image link"],None))
            
        RecommendedSeriesName= list(filter(None,RecommendedSeriesName))
        RecommendedSeriesImage= list(filter(None,RecommendedSeriesImage))
        
        #Displaying not watched TV series to the user as recommendations
        st.header("Recommended for You")
        Checklist=[]
        for i in range (0,(len(RecommendedSeriesName))):
            if ((RecommendedSeriesName[i] not in SeriesWatched) and (RecommendedSeriesName[i] not in Checklist) ): 
                Checklist=Checklist + list(RecommendedSeriesName[i])
                st.text(RecommendedSeriesName[i])
                st.image(RecommendedSeriesImage[i],width=200)
        
        #Displaying already watched TV series for USers information
        st.header("Already Watched")
        for i in range (0,(len(SeriesWatched))):
            st.text(SeriesWatched[i])
            st.image(SeriesWatchedImage[i],width=200)
         
        #Machine learning Association apriori algorithm to check TV series bundle connections
       # user_data_new=user_data.drop(columns=["Username"])
        #recommended = [] 
        #temp=[]
        #for i in range(0,user_data_new.shape[0]): 
         #   temp=[] 
          #  for j in range(0,user_data_new.shape[1]): 
           #     if str(user_data_new.values[i,j])!='0':
            #        temp.append(str(user_data_new.values[i,j])) 
            #recommended.append(temp)
        
       # association_rules = list(apriori(recommended,min_support=0.2, min_confidence=0.3))
        
        #Saving the ML code as excel output
        #recommendations_outcomes = pd.DataFrame(association_rules)
        #recommendations_outcomes.to_excel("Watch_NOW recommendations.xlsx")
        
   
   
    
   
    
   #Incase of error display this
    else:
        st.text("Please select appropriate page")

    



    #RESPONSE SECTION
    st.title('Response Section')
    st.text('Leave a Feedback')
    st.number_input("Rate our application",min_value=1.0, max_value=5.0,step=1.0) 
    address = st.text_area("Additional comments you like to give us")
    if st.checkbox("I confirm my response",value = False):
       st.write("Thanks for giving feedback") 
       
    #Page Footer
    st.text("Created by Working Group-3")
    st.button("Submit")
    
#If the login credentials are incorrect
elif (UserName!="" and Password!=""):
    st.text("Login Credentials Incorrect")
    
#If user has not logged in
else:
    st.text("Please Login")
