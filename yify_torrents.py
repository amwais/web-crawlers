#!/usr/bin/python

from bs4 import BeautifulSoup
import requests

base = "https://yts.ag/browse-movies/0/all/all/7/latest"
suffix = "?page="

print('\n')


def crawl_pages(max_page):
    for n in range(1,max_page+1):
        if n < 2:
            url = base
        else:
            url = base+suffix+str(n)

        html = requests.get(url).text
        # print "Accessing: " + url

        soup = BeautifulSoup(html, 'html.parser')


        all_links = soup.find_all('a', {'class': 'browse-movie-title'})
        all_ratings = soup.find_all('h4', {'class': 'rating'})
        div_tags = soup.find_all('div', {'class': 'browse-movie-tags'})
        all_years = soup.find_all('div', {'class': 'browse-movie-year'})

        for i in range(len(all_links)):
            title = all_links[i].string
            rtScores = get_rt_scores(title)
            year = all_years[i].string
            print(title, "|", year, "|", "IMDB Score: " + all_ratings[i].string.split(" / 10")[0], "|", "RT Scores:", rtScores)
            print(div_tags[i].contents[1].get('href'), "\n")


def get_rt_scores(movie_title):

    if movie_title[:3] == "the":
        movie_title = movie_title.split("the ")[1]

    movie_search_term = movie_title.replace("'", "")
    movie_search_term = movie_search_term.replace(" ", "_")
    url = base + movie_search_term
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    critic = soup.find('span', {'class': 'meter-value superPageFontColor'})
    audience = soup.find('div', {'class': 'audience-score meter'})
    try:
        critic_score = critic.text[:1] + "." + critic.text[1:-1]
        audience = audience.contents[1].contents[0].contents[3].contents[1].text
        audience_score = audience[1] + "." + audience[2:-2]

        avg_score = str(((float(critic_score) + float(audience_score)) / 2))

        return ["Critics: "+str(critic_score), "Audience: "+ str(audience_score), "Average: " + avg_score]
    except:
        try:
            movie_search_term = movie_title.replace("'", "")
            movie_search_term = movie_search_term.replace(" ", "-")
            url = base + movie_search_term
            html = requests.get(url).text
            soup = BeautifulSoup(html, 'html.parser')

            critic = soup.find('span', {'class': 'meter-value superPageFontColor'})
            audience = soup.find('div', {'class': 'audience-score meter'})

            critic_score = critic.text[:1] + "." + critic.text[1:-1]
            audience = audience.contents[1].contents[0].contents[3].contents[1].text
            audience_score = audience[1] + "." + audience[2:-2]

            avg_score = str(((float(critic_score) + float(audience_score)) / 2))

            # print "\nTomatometer: " + critic_score
            # print "Audience score: " + audience_score
            #
            # print "\nCalculated score: " + avg_score

            return ["Critics: "+str(critic_score), "Audience: "+ str(audience_score), "Average: " + avg_score]
        except:
            pass


crawl_pages(3)
