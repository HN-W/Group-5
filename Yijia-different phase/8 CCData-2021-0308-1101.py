# import modules 
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cm
get_ipython().run_line_magic('matplotlib', 'inline')

# #### `CCData2018-2021` 
# **Summary**: 654915 user's behavior dataset between January 2018 and November 2021.    
# **Data type**: tabular  
# **Rows**: 654915 rows, each row representing one user action.   
# **Columns**: 9 columns. Which is `Time`, `VisitorID`, `ExternalID`, `Role`, `Location`, `Link Title`, `Link Type`, `ContentInfo`, `URL`    
# **Value Type**: String.   
# **Time Frame**: There is data here going back to January 2018 until November 2021.   
# **Links**: This file can use 'External ID' to link to `User2021` and `CustomerMedicalConditions`, and use 'Visiter ID' to link to `User2021`.   
#  
# #### `User2021`
# **Summary**: 3641 user information dataset in 2021     
# **Data type**: tabular   
# **Rows**: 3641 rows of data, each row representing one user's information      
# **Columns**: 6 columns. Which is `User ID`, `VisitorID`, `External ID`, `Birth date`, `Gender`, `Location`       
# **Value Type**: String.    
# **Time Frame**: The data in this file only show the user still alive in 2021.   
# **Links**: This file can use 'External ID' to link to `CCData2018-2021` and `CustomerMedicalConditions`, and use 'Visiter ID' to link to `CCData2018-2021`.    
# 
# 
# #### `CustomerMedicalConditions` 
# **Summary**: 1312 user health status dataset    
# **Data type**: tabular    
# **Rows**: 1312 rows of data, each row representing one user's helath information (one user may have several rows)    
# **Columns**: 7 columns. Which is `External ID`, `CleverCogsUserId`, `Gender`, `DateOfBirth`, `Age`, `StaffPlanConditions`, `CareSysCondition`    
# **Value Type**: String.     
# **Time Frame**: The data in this file only show the user still alive in 2021.    
# **Links**: This file can use 'External ID' to link to `CCData2018-2021` and `User2021`.     

#Convert two Excel files into CSV files, uploading to notebook and loading the files.
CCDate_2021_Data = pd.read_csv("CCDate2018-2021-3-8.csv")
CMC_2021_Data = pd.read_csv("CustomerMedicalConditions04Nov21.csv")

# Delete data other than 'user' in 'Role'
Role_notUser_list=[]
for x in range(len(CCDate_2021_Data.index)):
    if CCDate_2021_Data.iloc[x,2] !='User':
#         print(CCDate_2021_Data.iloc[x,2])
        Role_notUser_list.append(x)
# print(Role_notUser_list)
CCDate_2021_Data_ClRole=CCDate_2021_Data.drop(Role_notUser_list)
print('done')
CCDate_2021_Data_ClRole

#Delete 'NULL' in 'ExternalID'
CCDate_2021_Data_ClRole_ClEx = CCDate_2021_Data_ClRole.dropna(axis = 0, subset = ['ExternalID'])
print('done')
CCDate_2021_Data_ClRole_ClEx

# I find that some 'External ID' have several rows
ID_counts = CMC_2021_Data['ExternalID'].value_counts()
print(ID_counts)

# Delete duplicate data in 'External ID'
CMC_2021_Data_OnlyID = CMC_2021_Data.drop_duplicates(['ExternalID'])
CMC_2021_Data_OnlyID

# inner merge CCDate_2021_Data_ClRole_ClEx and CMC_2021_Data_OnlyID
CCDate_CMC_2021_inner = pd.merge(CCDate_2021_Data_ClRole_ClEx, CMC_2021_Data_OnlyID, on='ExternalID', how='inner')
print('done')
CCDate_CMC_2021_inner

# Age distribution
pic = plt.figure(figsize=(10,5),dpi=80) 
fig1 = pic.add_subplot(1,2,1)
age_displot = sns.distplot(CMC_2021_Data_OnlyID['Age'])
age_displot.set_title('Age distribution plot')
fig2 = pic.add_subplot(1,2,2)
age_boxplot = sns.boxplot(CMC_2021_Data_OnlyID['Age'])
age_boxplot.set_title('Age box plot')
plt.show()

# Method of showing both values and percentages in a pie chart
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct


# Gender distribution
pic = plt.figure(figsize=(7,7),dpi=80)
gender_counts = CMC_2021_Data_OnlyID['Gender'].value_counts()
plt.pie(gender_counts, labels = gender_counts.index, startangle = 90, counterclock = False, autopct=make_autopct(gender_counts));
plt.show()

# CareSysCondition distributon
pic = plt.figure(figsize=(7,7),dpi=80)
CSC_counts = CMC_2021_Data_OnlyID['CareSysCondition'].value_counts()
plt.pie(CSC_counts, labels = CSC_counts.index, startangle = 90, counterclock = False, autopct=make_autopct(CSC_counts));
plt.show()

# StaffPlanConditions distributon
pic = plt.figure(figsize=(7,7),dpi=80)
SPC_counts = CMC_2021_Data['StaffPlanConditions'].value_counts()
SPC_counts_clean=SPC_counts[SPC_counts>3] #Too small data filtered out, too small data not clearly displayed in the pie chart
plt.pie(SPC_counts_clean, labels = SPC_counts_clean.index, startangle = 90, counterclock = False, autopct=make_autopct(SPC_counts_clean));
plt.show()
# print(SPC_counts)

# Usage of each ExternalID 
pic = plt.figure(figsize=(7,7),dpi=80)
ExternalID_counts = CCDate_2021_Data_ClRole_ClEx['ExternalID'].value_counts()
plt.pie(ExternalID_counts, labels = ExternalID_counts.index, startangle = 90, counterclock = False, autopct=make_autopct(ExternalID_counts));
plt.show()

# LinkType Distribution
pic = plt.figure(figsize=(5,5),dpi=80)
LinkType_counts = CCDate_2021_Data_ClRole_ClEx['LinkType'].value_counts()
plt.pie(LinkType_counts, labels = LinkType_counts.index, startangle = 90, counterclock = False, autopct=make_autopct(LinkType_counts));
plt.show()
print(LinkType_counts)

# LinkTitle Distribution
pic = plt.figure(figsize=(7,7),dpi=80) 
LinkTitle_counts = CCDate_2021_Data_ClRole_ClEx['LinkTitle'].value_counts()
a=LinkTitle_counts[LinkTitle_counts>1000] # Cleaning out too small data
plt.pie(a, labels = a.index, startangle = 90, counterclock = False, autopct=make_autopct(a))
plt.show()

# Location Distribution
pic = plt.figure(figsize=(7,7),dpi=80) 
Location_counts = CCDate_2021_Data_ClRole_ClEx['Location'].value_counts()
plt.pie(Location_counts, labels = Location_counts.index, startangle = 90, counterclock = False, autopct=make_autopct(Location_counts));
plt.show()

# Relationships between Variables Analysed

# 1. Usage amount per month**    
# Usage amount per month
pic = plt.figure(figsize=(10,6),dpi=80) 

Usage_amount_data_list = []
Usage_amount_month_list = []

# Identify the month and generate the dataset by identifying the beginning of the Time list string
for x in range(3, 12): 
    Usage_amount_data_list.append(len(CCDate_2021_Data_ClRole_ClEx[CCDate_2021_Data_ClRole_ClEx['Time'].str.startswith(str(x))]))
    Usage_amount_month_list.append(x)

plt.bar(range(len(Usage_amount_data_list)), Usage_amount_data_list, tick_label = Usage_amount_month_list)

plt.xlabel("Month (2021)")  # Set X-axis Y-axis name  
plt.ylabel("Usage amount") 

for a,b in zip(range(len(Usage_amount_data_list)),Usage_amount_data_list):  # Use text to display values 
    plt.text(a, b+0.05, '%.0f' % b, ha='center', va='bottom',fontsize=10) 

plt.show()

# **2. Usage amount by male and female per month**      
# Usage amount by male and female per month
pic = plt.figure(figsize=(10,6),dpi=80) 

Usage_amount_data_list_male = []
Usage_amount_data_list_female = []
Usage_amount_month_list = []

# Identify the month and gender and generate the dataset by identifying the beginning of the Time list string
for x in range(3, 12):
    a=CCDate_CMC_2021_inner[CCDate_CMC_2021_inner['Time'].str.startswith(str(x))]
    Usage_amount_data_list_male.append(len(a[a['Gender']=='M']))
    Usage_amount_data_list_female.append(len(a[a['Gender']=='F']))
    Usage_amount_month_list.append(x)

list_len =list(range(len(Usage_amount_data_list_male)))
total_width, n = 0.8, 2
width = total_width / n

plt.bar(list_len, Usage_amount_data_list_male, width=width, label='Male', fc = 'y')
for i in range(len(list_len)):
    list_len[i] = list_len[i] + width
plt.bar(list_len, Usage_amount_data_list_female, width=width, label='Female',tick_label = Usage_amount_month_list,fc = 'r')

plt.xlabel("Month (2021)")  # Set X-axis Y-axis name  
plt.ylabel("Usage amount") 

for a,b in zip(range(len(Usage_amount_data_list_male)),Usage_amount_data_list_male):  # Use text to display values 
    plt.text(a, b+0.05, '%.0f' % b, ha='center', va='bottom',fontsize=10) 
    
for a,b in zip(range(len(Usage_amount_data_list_female)),Usage_amount_data_list_female):  # Use text to display values 
    plt.text(a+0.4, b+0.05, '%.0f' % b, ha='center', va='bottom',fontsize=10) 

plt.legend()
plt.show()

# **3. Health condition for different age groups**      

# Health condition for different age groups
pic2 = plt.figure(figsize=(20,20),dpi=80) 

x=0 # Age group
y=1 # Subplots

while x<110:
    a=CMC_2021_Data_OnlyID[(CMC_2021_Data_OnlyID['Age']>=x) & (CMC_2021_Data_OnlyID['Age']<(x+10))]
    CSC_counts=a['CareSysCondition'].value_counts(dropna=False)
#     print(CSC_counts)
    
    fig1 = pic2.add_subplot(4,3,y) # Subplots
    plt.pie(CSC_counts, labels = CSC_counts.index, startangle = 90, counterclock = False, autopct=make_autopct(CSC_counts));
    
    s = 'Age: {n}-{m}'
    plt.title(s.format(n=x, m=x+9),fontsize=12)
    
    x+=10 # Age group +10
    y+=1 # Subplots +1

plt.show()

# **4. LinkTitle Distribution in 'Internet' and 'Category'**      

# LinkTitle Distribution in 'Internet' and 'Category'
pic = plt.figure(figsize=(10,5),dpi=80) 

CCDate_2021_Data_ClRole_ClEx_Internet=CCDate_2021_Data_ClRole_ClEx[CCDate_2021_Data_ClRole_ClEx['LinkType']=='Internet']['LinkTitle']
CCDate_2021_Data_ClRole_ClEx_Category=CCDate_2021_Data_ClRole_ClEx[CCDate_2021_Data_ClRole_ClEx['LinkType']=='Category']['LinkTitle']

LinkTitle_counts_Internet = CCDate_2021_Data_ClRole_ClEx_Internet.value_counts()
LinkTitle_counts_Category = CCDate_2021_Data_ClRole_ClEx_Category.value_counts()

LinkTitle_counts_Internet_clean=LinkTitle_counts_Internet[LinkTitle_counts_Internet>1000] #清洗掉过小的数据
LinkTitle_counts_Category_clean=LinkTitle_counts_Category[LinkTitle_counts_Category>1000]

fig1 = pic.add_subplot(1,2,1)
plt.pie(LinkTitle_counts_Internet_clean, labels = LinkTitle_counts_Internet_clean.index, startangle = 90, counterclock = False, autopct=make_autopct(LinkTitle_counts_Internet_clean));
plt.title('LinkTitle Distribution in Internet',fontsize=12)

fig2 = pic.add_subplot(1,2,2)
plt.pie(LinkTitle_counts_Category_clean, labels = LinkTitle_counts_Category_clean.index, startangle = 90, counterclock = False, autopct=make_autopct(LinkTitle_counts_Category_clean));
plt.title('LinkTitle Distribution in Category',fontsize=12)

plt.show()

# ### Hypothesise
# ####  Hypotheses1: There were events in June that female have more interest, such as discounts on merchandise, resulting in much higher usage by female than male in June.
# 
# The 'usage amount' of female users generally a little more than male users'. But in June, the 'usage amount' of female users much more than male users', even more than three times. (Female: 9277, Male: 3614)       
# So, maybe there were some events that female user want to do more on the platform.        
# Further research may be needed on how user behaviour in June differs from other months, user interviews, asking data holders.
# 
# ![image.png](attachment:image.png)
# 
# 
# #### Hypotheses2: Healthy elderly people are the largest user group
# User who only require 'Elderly Care/support' rank the first (29.59%), maybe the largest user group is healthy elderly people.          
# Further research may be needed on asking data holder whether those user are healthy.            
# ![image-2.png](attachment:image-2.png)
# 
# #### Hypotheses3: The user in bigger city are more active?
# The five regions with the highest levels of activity are in big city like Edinburgh, Glasgow, etc. So maybe the user in bigger city are more active.          
# The reason might be that the larger the city, the greater the user needs and the larger the facilities opened, the more users there will be and so more active.         
# Further research may be needed on the city pupolation, CleverCogs' facilities.        
# ![image-4.png](attachment:image-4.png)
# 
# #### Hypotheses4: The reason for the high proportion of 'mental health' among young people is the lockdown
# Among the health problems of users younger than 70, 'Mental Health issues' is the most important problem.       
# Maybe because the lockdown, people go out or hung out with their friends less often, leading to mental health issues.       
# Further research may be needed on comparing with the date before the lockdown.       
# ![image-6.png](attachment:image-6.png)
# 
# #### Hypotheses5: Users younger than 10 years old may be relatives of staff members
# The majority of the data were adults. But there were seven outliers younger than 10 years old and only one of them had a health problem, the remaining six had no health problems. If they are not old or do not have health problem, Why are they become the users of CleverCogs?
# 
# Maybe the user younger than 10 years old is relative of staff members, for some kind of convenience to register CleverCogs.
# 
# Further research may be needed on know more about these users' behavior, asking data holder. 
# 
# ![image-7.png](attachment:image-7.png)