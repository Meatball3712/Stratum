from Stories import stories, openStory
import argparse

parser = argparse.ArgumentParser(description="ETL Master Program - run all modules sequentially.")
parser.add_argument('-d', '--debug', dest='debug', action='store_const', const=True, default=False, help= "Perform debug testing instead of actually submitting.")
parser.add_argument('-s', '--story', dest='story', action='store', default=False, help= "Story Name")
kwargs = vars(parser.parse_args())

if kwargs["story"]:
    S = kwargs.["story"]
else:
    # Tell us a story
    choices = []
    ans = -1

    while ans < choices or ans > choices:
        print("The following stories are available.")

        for story in stories.keys():
            print("{}: {}".format(len(choices), stories[story]))
            choices.append(story)

        try:
            ans = int(raw_input("Which story would you like me to read?"))
        except ValueError:
            print "That is not a valid number."
    S = choices[ans]

# Got answer. Read story.
story = openStory(S)

story.read()