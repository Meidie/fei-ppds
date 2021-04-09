def complain_about(substring):
    print("Please talk to me!")
    try:
        while True:
            text = (yield)
            print(text)
            if substring in text:
                print(f"Oh no: I found a [{substring}] again!")
    except GeneratorExit:
        print("Ok I am quitting.")


def main():
    coroutine = complain_about("the")
    print(coroutine)
    coroutine.send(None)  # next(coroutine)

    coroutine.send("To spot the expert, pick the one who predicts the job will"
                   " take the longest and cost the most")
    coroutine.send("Logic is a systematic method of coming to the wrong"
                   " conclusion with confidence.")
    coroutine.send("Any system which depends on human reliability"
                   " is unreliable")
    coroutine.send("When all else fails, read the instructions")
    coroutine.close()


if __name__ == "__main__":
    main()
