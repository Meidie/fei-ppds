from time import sleep
from random import randint
from fei.ppds import Semaphore, Thread, Mutex, print


class Shared:
    def __init__(self):
        self.tobacco = Semaphore(0)
        self.paper = Semaphore(0)
        self.match = Semaphore(0)

        self.agentSem = Semaphore(1)

        self.isTobacco = False
        self.isPaper = False
        self.isMatch = False

        self.tobacco_dealer = Semaphore(0)
        self.paper_dealer = Semaphore(0)
        self.match_dealer = Semaphore(0)

        self.mutex = Mutex()


def make_cigarette(who):
    print("\t%s makes cigarette" % who)
    sleep(randint(0, 10) / 100)


def smoke(who):
    print("\t%s smokes" % who)
    sleep(randint(0, 10) / 100)


def agent_1(shared: Shared):
    while True:
        sleep(randint(0, 10) / 100)
        shared.agentSem.wait()
        print("agent: tobacco, paper --> smoker_match")
        shared.tobacco.signal()
        shared.paper.signal()


def agent_2(shared: Shared):
    while True:
        sleep(randint(0, 10) / 100)
        shared.agentSem.wait()
        print("agent: paper, match --> smoker_tobacco")
        shared.paper.signal()
        shared.match.signal()


def agent_3(shared: Shared):
    while True:
        sleep(randint(0, 10) / 100)
        shared.agentSem.wait()
        print("agent: tobacco, match --> smoker_paper")
        shared.tobacco.signal()
        shared.match.signal()


def smoker_match(shared: Shared):
    while True:
        sleep(randint(0, 10) / 100)
        shared.match_dealer.wait()
        make_cigarette("smoker_match")
        shared.agentSem.signal()
        smoke("smoker_match")


def smoker_tobacco(shared: Shared):
    while True:
        sleep(randint(0, 10) / 100)
        shared.tobacco_dealer.wait()
        make_cigarette("smoker_tobacco")
        shared.agentSem.signal()
        smoke("smoker_tobacco")


def smoker_paper(shared: Shared):
    while True:
        sleep(randint(0, 10) / 100)
        shared.paper_dealer.wait()
        make_cigarette("smoker_paper")
        shared.agentSem.signal()
        smoke("smoker_paper")


def dealer_tobacco(shared: Shared):
    while True:
        shared.tobacco.wait()
        shared.mutex.lock()

        if shared.isPaper:
            shared.isPaper = False
            shared.match_dealer.signal()
        elif shared.isMatch:
            shared.isMatch = False
            shared.paper_dealer.signal()
        else:
            shared.isTobacco = True

        shared.mutex.unlock()


def dealer_paper(shared: Shared):
    while True:
        shared.paper.wait()
        shared.mutex.lock()

        if shared.isMatch:
            shared.isMatch = False
            shared.tobacco_dealer.signal()
        elif shared.isTobacco:
            shared.isTobacco = False
            shared.match_dealer.signal()
        else:
            shared.isPaper = True

        shared.mutex.unlock()


def dealer_match(shared: Shared):
    while True:
        shared.match.wait()
        shared.mutex.lock()

        if shared.isTobacco:
            shared.isTobacco = False
            shared.paper_dealer.signal()
        elif shared.isPaper:
            shared.isPaper = False
            shared.tobacco_dealer.signal()
        else:
            shared.isMatch = True

        shared.mutex.unlock()


def create_threads(shared: Shared, smokers: list, agents: list, dealers: list):

    dealers.append(Thread(dealer_match, shared))
    dealers.append(Thread(dealer_tobacco, shared))
    dealers.append(Thread(dealer_paper, shared))

    smokers.append((Thread(smoker_match, shared)))
    smokers.append(Thread(smoker_tobacco, shared))
    smokers.append(Thread(smoker_paper, shared))

    agents.append(Thread(agent_1, shared))
    agents.append(Thread(agent_2, shared))
    agents.append(Thread(agent_3, shared))


def wait_to_finish(smokers: list, agents: list, dealers: list):
    for t in smokers + dealers + agents:
        t.join()


def main():
    shared = Shared()
    smokers, dealers, agents = list(), list(), list()

    create_threads(shared, smokers, agents, dealers)
    wait_to_finish(smokers, agents, dealers)


if __name__ == '__main__':
    main()
