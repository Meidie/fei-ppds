from time import sleep
from random import randint
from fei.ppds import Semaphore, Thread, print


class Shared:
    def __init__(self):
        self.tobacco = Semaphore(0)
        self.paper = Semaphore(0)
        self.match = Semaphore(0)
        self.agentSem = Semaphore(1)


def make_cigarette():
    sleep(randint(0, 10) / 100)


def smoke():
    sleep(randint(0, 10) / 100)


def agent_1(shared: Shared):
    while True:
        sleep(randint(0, 10) / 100)

        shared.agentSem.wait()
        print("agent: tobacco, paper")
        shared.tobacco.signal()
        shared.paper.signal()


def agent_2(shared: Shared):
    while True:
        sleep(randint(0, 10) / 100)

        shared.agentSem.wait()
        print("agent: paper, match")
        shared.paper.signal()
        shared.match.signal()


def agent_3(shared: Shared):
    while True:
        sleep(randint(0, 10) / 100)

        shared.agentSem.wait()
        print("agent: tobacco, match")
        shared.tobacco.signal()
        shared.match.signal()


def smoker_match(shared: Shared):
    while True:
        sleep(randint(0, 10) / 100)
        shared.paper.wait()
        print("\ts_m:  paper")
        shared.tobacco.wait()
        print("\ts_m: tobacco")
        make_cigarette()
        shared.agentSem.signal()
        smoke()


def smoker_tobacco(shared: Shared):
    while True:
        sleep(randint(0, 10) / 100)
        shared.match.wait()
        print("\ts_t:  match")
        shared.paper.wait()
        print("\ts_t:  paper")
        make_cigarette()
        shared.agentSem.signal()
        smoke()


def smoker_paper(shared: Shared):
    while True:
        sleep(randint(0, 10) / 100)
        shared.tobacco.wait()
        print("\ts_p: tobacco")
        shared.match.wait()
        print("\ts_p:  match")
        make_cigarette()
        shared.agentSem.signal()
        smoke()


def create_smokers_and_agents(shared: Shared, smokers: list, agents: list):

    smokers.append((Thread(smoker_match, shared)))
    smokers.append(Thread(smoker_tobacco, shared))
    smokers.append(Thread(smoker_paper, shared))

    agents.append(Thread(agent_1, shared))
    agents.append(Thread(agent_2, shared))
    agents.append(Thread(agent_3, shared))


def wait_to_finish(smokers: list, agents: list):
    for s in smokers:
        s.join()

    for a in agents:
        a.join()


def main():
    shared = Shared()
    smokers, agents = list(), list()

    create_smokers_and_agents(shared, smokers, agents)
    wait_to_finish(smokers, agents)


if __name__ == '__main__':
    main()
