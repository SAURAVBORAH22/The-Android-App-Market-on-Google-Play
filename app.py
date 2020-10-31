import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import plotly
plotly.offline.init_notebook_mode(connected=True)
import plotly.graph_objs as go
st.set_option('deprecation.showPyplotGlobalUse', False)
import seaborn as sns
import matplotlib.pyplot as plt


def main():
    activities=['Google Play Store apps and review','Developer']
    option=st.sidebar.selectbox('Menu Bar:',activities)
    if option=='Google Play Store apps and review':
        html_temp = """
        <div style = "background-color: Yellow; padding: 10px;">
            <center><h1>Google Play Store apps and review</h1></center>
        </div><br>
        """
        st.markdown(html_temp, unsafe_allow_html=True)
        st.write('Mobile apps are everywhere. They are easy to create and can be lucrative. Because of these two factors, more and more apps are being developed. In this notebook, I did a comprehensive analysis of the Android app market by comparing over ten thousand apps in Google Play across different categories. I looked for insights in the data to devise strategies to drive growth and retention.')
        image=Image.open('1.jpg')
        st.image(image,use_column_width=True)
        st.write('Let\'s take a look at the data, which consists of two files:')
        st.write('1.**apps.csv**: contains all the details of the applications on Google Play. There are 13 features that describe a given app.')
        st.write('2.**user_reviews.csv**: contains 100 reviews for each app, most helpful first. The text in each review has been pre-processed and attributed with three new features: Sentiment (Positive, Negative or Neutral), Sentiment Polarity and Sentiment Subjectivity.')


        apps_with_duplicates =pd.read_csv("apps.csv")
        # Drop duplicates
        apps =apps_with_duplicates.drop_duplicates()
        # Print the total number of apps
        st.write('Total number of apps in the dataset:')
        st.write(apps['App'].count())
        st.subheader('Let\'s have a look at a random sample of 5 rows:')
        n = 5
        st.write(apps.sample(n)) 

        st.header('Data Cleaning')
        st.write('The three features that we will be working with most frequently henceforth are Installs, Size, and Price. A careful glance of the dataset reveals that some of these columns mandate data cleaning in order to be consumed by code later. Specifically, the presence of special characters (, $ +) and letters (M k) in the Installs, Size, and Price columns make their conversion to a numerical data type difficult. Let\'s clean by removing these and converting each column to a numeric type.')
        # List of characters to remove
        chars_to_remove = ["+",",","M","$"]
        # List of column names to clean
        cols_to_clean = ["Installs","Size","Price"]

        # Loop for each column
        for col in cols_to_clean:
            # Replace each character with an empty string
            for char in chars_to_remove:
                apps[col] = apps[col].str.replace(char, '')
            # Convert col to numeric
            apps[col] = pd.to_numeric(apps[col]) 
        

        st.header('Exploring app categories')
        st.write('With more than 1 billion active users in 190 countries around the world, Google Play continues to be an important distribution platform to build a global audience. For businesses to get their apps in front of users, it\'s important to make them more quickly and easily discoverable on Google Play. To improve the overall search experience, Google has introduced the concept of grouping apps into categories.')
        st.write('This brings us to the following questions:')
        st.write('**Which category has the highest share of (active) apps in the market?**')
        st.write('**Is any specific category dominating the market?**')
        st.write('**Which categories have the fewest number of apps?**')
        # Print the total number of unique categories
        num_categories = len(apps['Category'].unique())
        st.write('Number of categories:')
        st.write(num_categories)
        # Count the number of apps in each 'Category' and sort them in descending order
        num_apps_in_category = apps['Category'].value_counts().sort_values(ascending = False)
        data = [go.Bar(
                x = num_apps_in_category.index, # index = category name
                y = num_apps_in_category.values, # value = count
        )]
        st.plotly_chart(data)
        st.write('We will see that there are 33 unique app categories present in our dataset. Family and Game apps have the highest market prevalence. Interestingly, Tools, Business and Medical apps are also at the top.')


        st.header('Distribution of app ratings')
        st.write('After having witnessed the market share for each category of apps, let\'s see how all these apps perform on an average. App ratings (on a scale of 1 to 5) impact the discoverability, conversion of apps as well as the company\'s overall brand image. Ratings are a key performance indicator of an app.')
        # Average rating of apps
        avg_app_rating = apps['Rating'].mean()
        st.write('Average app rating:-')
        st.write(avg_app_rating)
        # Distribution of apps according to their ratings
        data = [go.Histogram(
                x = apps['Rating']
        )]
        # Vertical dashed line to indicate the average app rating
        layout = {'shapes': [{
                    'type' :'line',
                    'x0': avg_app_rating,
                    'y0': 0,
                    'x1': avg_app_rating,
                    'y1': 1000,
                    'line': { 'dash': 'dashdot'}
                }]
                }
        st.plotly_chart(data)
        st.write('From our research, we found that the average volume of ratings across all app categories is 4.17. The histogram plot is skewed to the right indicating that the majority of the apps are highly rated with only a few exceptions in the low-rated apps')


        st.header('Size and price of an app')
        st.write('Let\'s now examine app size and app price. For size, if the mobile app is too large, it may be difficult and/or expensive for users to download. Lengthy download times could turn users off before they even experience your mobile app. Plus, each user\'s device has a finite amount of disk space. For price, some users expect their apps to be free or inexpensive. These problems compound if the developing world is part of your target market; especially due to internet speeds, earning power and exchange rates.')
        st.write('How can we effectively come up with strategies to size and price our app?')
        st.write('**Does the size of an app affect its rating?**')
        st.write('**Do users really care about system-heavy apps or do they prefer light-weighted apps?**')
        st.write('**Does the price of an app affect its rating?**')
        st.write('**Do users always prefer free apps over paid apps?**')
        sns.set_style("darkgrid")
        # Subset for categories with at least 250 apps
        large_categories = apps.groupby(apps['Category']).filter(lambda x: len(x) >= 250).reset_index()

        # Plot size vs. rating
        st.subheader('Size vs. Rating')
        plt1 = sns.jointplot(x = large_categories['Size'], y = large_categories['Rating'], kind = 'hex')
        st.pyplot(plt1)

        # Subset out apps whose type is 'Paid'
        paid_apps = apps[apps['Type'] == 'Paid']

        # Plot price vs. rating
        st.subheader('Price vs. Rating')
        plt2 = sns.jointplot(x = paid_apps['Price'], y = paid_apps['Rating'])
        st.pyplot(plt2)

        st.write('We find that the majority of top rated apps (rating over 4) range from 2 MB to 20 MB. We also find that the vast majority of apps price themselves under \$10.')

        st.header('Relation between app category and app price')
        st.write('So now comes the hard part. How are companies and developers supposed to make ends meet? What monetization strategies can companies use to maximize profit? The costs of apps are largely based on features, complexity, and platform.')
        st.write('There are many factors to consider when selecting the right pricing strategy for your mobile app. It is important to consider the willingness of your customer to pay for your app. A wrong price could break the deal before the download even happens. Potential customers could be turned off by what they perceive to be a shocking cost, or they might delete an app they’ve downloaded after receiving too many ads or simply not getting their money\'s worth.')
        st.write('Different categories demand different price ranges. Some apps that are simple and used daily, like the calculator app, should probably be kept free. However, it would make sense to charge for a highly-specialized medical app that diagnoses diabetic patients. Below, we see that Medical and Family apps are the most expensive. Some medical apps extend even up to \$80! All game apps are reasonably priced below \$20.')
        fig, ax = plt.subplots()
        fig.set_size_inches(15, 8)

        # Select a few popular app categories
        popular_app_cats = apps[apps.Category.isin(['GAME', 'FAMILY', 'PHOTOGRAPHY',
                                                    'MEDICAL', 'TOOLS', 'FINANCE',
                                                    'LIFESTYLE','BUSINESS'])]

        # Examine the price trend by plotting Price vs Category
        st.subheader('Price vs Category')
        ax = sns.stripplot(x = popular_app_cats['Price'], y = popular_app_cats['Category'], jitter=True, linewidth=1)
        ax.set_title('App pricing trend across categories')
        st.pyplot()

        # Apps whose Price is greater than 200
        apps_above_200 = popular_app_cats[['Category', 'App', 'Price']][popular_app_cats['Price'] > 200]
        st.subheader('Apps whose Price is greater than 200:')
        st.write(apps_above_200)

        st.header('Filter out "junk" apps')
        st.write('It looks like a bunch of the really expensive apps are "junk" apps. That is, apps that don\'t really have a purpose. Some app developer may create an app called I Am Rich Premium or most expensive app (H) just for a joke or to test their app development skills. Some developers even do this with malicious intent and try to make money by hoping people accidentally click purchase on their app in the store.')
        st.write('Let\'s filter out these junk apps and re-do our visualization. The distribution of apps under \$20 becomes clearer')

        # Select apps priced below $100
        apps_under_100 = popular_app_cats[popular_app_cats['Price'] < 100]

        fig, ax = plt.subplots()
        fig.set_size_inches(15, 8)

        # Examine price vs category with the authentic apps
        ax = sns.stripplot(x='Price', y='Category', data=popular_app_cats,
                        jitter=True, linewidth=1)
        ax.set_title('App pricing trend across categories after filtering for junk apps')
        st.pyplot()


        st.header('Popularity of paid apps vs free apps')
        st.write('For apps in the Play Store today, there are five types of pricing strategies: free, freemium, paid, paymium, and subscription. Let\'s focus on free and paid apps only.')
        st.subheader('Some characteristics of free apps are:')
        st.write('1.Free to download.')
        st.write('2.Main source of income often comes from advertisements')
        st.write('3.Often created by companies that have other products and the app serves as an extension of those products.')
        st.write('4.Can serve as a tool for customer retention, communication, and customer service')
        st.subheader('Some characteristics of paid apps are:')
        st.write('1.Users are asked to pay once for the app to download and use it.')
        st.write('2.The user can\'t really get a feel for the app before buying it.')
        st.write('**Are paid apps installed as much as free apps? It turns out that paid apps have a relatively lower number of installs than free apps, though the difference is not as stark as I would have expected!**')
        trace0 = go.Box(
        # Data for paid apps
        y=apps[apps['Type'] =='Paid']['Installs'],
        name = 'Paid'
        )

        trace1 = go.Box(
            # Data for free apps
            y=apps[apps['Type'] == 'Free']['Installs'],
            name = 'Free'
        )

        layout = go.Layout(
            title = "Number of downloads of paid apps vs. free apps",
            yaxis = dict(
                type = 'log',
                autorange = True
            )
        )

        # Add trace0 and trace1 to a list for plotting
        data = [trace0,trace1]
        st.plotly_chart(data)

        st.header(' Sentiment analysis of user reviews')
        st.write('Mining user review data to determine how people feel about your product, brand, or service can be done using a technique called sentiment analysis. User reviews for apps can be analyzed to identify if the mood is positive, negative or neutral about that app. For example, positive words in an app review might include words such as \'amazing\',\'friendly\', \'good\', \'great\', and \'love\'. Negative words might be words like \'malware\', \'hate\', \'problem\', \'refund\', and \'incompetent\'.')
        # Load user_reviews.csv
        reviews_df = pd.read_csv("user_reviews.csv")

        # Join and merge the two dataframe
        merged_df = pd.merge(apps,reviews_df , on ="App", how = "inner")

        # Drop NA values from Sentiment and Translated_Review columns
        merged_df = merged_df.dropna(subset=['Sentiment', 'Translated_Review'])

        sns.set_style('ticks')
        fig, ax = plt.subplots()
        fig.set_size_inches(11, 8)

        # User review sentiment polarity for paid vs. free apps
        ax = sns.boxplot(x = 'Type', y = 'Sentiment_Polarity', data =merged_df)
        ax.set_title('Sentiment Polarity Distribution')
        st.pyplot()

        st.write('By plotting sentiment polarity scores of user reviews for paid and free apps, we observe that free apps receive a lot of harsh comments, as indicated by the outliers on the negative y-axis. Reviews for paid apps appear never to be extremely negative. This may indicate something about app quality, i.e., paid apps being of higher quality than free apps on average. The median polarity score for paid apps is a little higher than free apps, thereby syncing with our previous observation.')
        st.write('In this notebook, we analyzed over ten thousand apps from the Google Play Store. We can use our findings to inform our decisions should we ever wish to create an app ourselves.')


    elif option=='Developer':
        html_temp = """
        <div style = "background-color: Cyan; padding: 10px;">
            <center><h1>Developer Section</h1></center>
        </div><br>
        """
        st.markdown(html_temp, unsafe_allow_html=True)
        st.balloons()
        st.title('Prepared by :-')
        st.header('SAURAV BORAH :sunglasses:')
        st.subheader('Source code for this project :- ')
        st.write('https://github.com/SAURAVBORAH22/The-Android-App-Market-on-Google-Play')
        st.subheader('My LinkedIn Profile:-')
        st.write('https://www.linkedin.com/in/saurav-borah-a7751818b/')


if __name__=='__main__':
    main()
