from locust import HttpUser, task, between
from server import competitions, clubs


class ProjectPerfTest(HttpUser):

    wait_time = between(3, 10)

    def on_start(self):
        self.client.get('/')

    def on_stop(self):
        self.client.get('/logout')

    @task
    def showSummaryLocust(self):
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task
    def bookLocust(self):
        competition = competitions[0]['name']
        club = clubs[0]['name']
        self.client.get(f'/book/{competition}/{club}')

    @task
    def purchasePlacesLocust(self):
        competition = competitions[0]['name']
        club = clubs[0]['name']
        places = 1
        self.client.post("/purchasePlaces", data={"competition": competition, "club": club, "places": places})

    @task
    def pointsDisplayBoardLocust(self):
        self.client.get("/pointsDisplayBoard")
