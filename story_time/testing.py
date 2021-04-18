__author__ = 'Peter LeBlanc'

from story.models import Line

def main():

    line = Line(text='There once was a girl who had a blue hat')
    line.save()


if __name__ == '__main__':
    main()
