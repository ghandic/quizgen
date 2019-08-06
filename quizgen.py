import json
import os
import argparse

from jinja2 import Environment, FileSystemLoader


class Quiz(object):

    def __init__(self, quiz):

        self.title = quiz.get("title", "Default quiz title")
        self.problem_sets = [ProblemSet(problem_set) for problem_set in quiz["problem_sets"]]
        self.total = sum([len(problem_set.questions) for problem_set in self.problem_sets])


class ProblemSet(object):

    def __init__(self, problem_set):
        self.title = problem_set.get("title", "Default problem set title")
        self.intro = problem_set.get("intro", "Default problem set intro")
        self.questions = [Question(question) for question in problem_set["questions"]]


class Question(object):

    def __init__(self, question):

        self.multiple = question.get("multiple", False)
        self.description = question.get("description", "Default question description")
        self.explanation = question.get("explanation", "Default question explanation")
        self.options = [Option(option) for option in question["options"]]


class Option(object):

    def __init__(self, option):

        self.description = option.get("description", "Default option description")
        self.correct = option["correct"]


def load_quiz(path):
    with open(path, 'r') as f:
        return Quiz(json.load(f))


def generate_standalone_quiz(path):
    env = Environment(loader=FileSystemLoader(["templates"]))
    t = env.get_template("quiz.html")
    return t.render(base_template="base.html", quiz=load_quiz(path))


def create_standalone_quiz_html(path):
    with open(os.path.splitext(path)[0] + '.html', 'w') as f:
        f.write(generate_standalone_quiz(path))


def get_args():
    parser = argparse.ArgumentParser(description="Commandline tool for compiling quizes")
    parser.add_argument('-i', '--input-quiz', required=True, help="Path to input quiz")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    create_standalone_quiz_html(args.input_quiz)
