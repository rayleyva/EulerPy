# -*- coding: utf-8 -*-

import os
import sys
import glob
import linecache

import click


base_name = '{0:0{w}d}{1}.{ext}'
dataDir = os.path.join(os.path.dirname(__file__), 'data')


class Problem(object):
    def __init__(self, problem_number):
        self.num = problem_number

    @property
    def filename(self, width=3, extension='py'):
        """Returns filename padded with leading zeros"""
        return base_name.format(self.num, '', w=width, ext=extension)


    def suf_name(self, suffix, width=3, extension='py'):
        """Similar to filename property but takes a suffix argument"""
        suffix = '-' + suffix
        return base_name.format(self.num, suffix, w=width, ext=extension)


    @property
    def iglob(self):
        """Returns a glob iterator for files belonging to a given problem"""
        return glob.iglob('{0:03d}*.py'.format(self.num))


    @property
    def solution(self):
        """Returns the answer to a given problem"""
        num = self.num

        solutionFile = os.path.join(dataDir, 'solutions.txt')
        solutionLine = linecache.getline(solutionFile, num)

        try:
            answer = solutionLine.split('. ')[1].strip()
        except IndexError:
            answer = None

        if answer:
            return answer
        else:
            msg = 'Answer for problem %i not found in solutions.txt.' % num
            click.secho(msg, fg='red')
            click.echo('If you have an answer, consider submitting a pull '
                       'request to EulerPy on GitHub.')
            sys.exit(1)


    @property
    def text(self):
        """Parses problems.txt and returns problem text"""
        def problem_iter(problem_num):
            problemFile = os.path.join(dataDir, 'problems.txt')

            with open(problemFile) as file:
                problemText = False
                lastLine = ''

                for line in file:
                    if line.strip() == 'Problem %i' % problem_num:
                        problemText = True

                    if problemText:
                        if line == lastLine == '\n':
                            break
                        else:
                            yield line[:-1]
                            lastLine = line

        problemLines = [line for line in problem_iter(self.num)]

        if problemLines:
            # First three lines are the problem number, the divider line,
            # and a newline, so don't include them in the returned string
            return '\n'.join(problemLines[3:])
        else:
            msg = 'Problem %i not found in problems.txt.' % self.num
            click.secho(msg, fg='red')
            click.echo('If this problem exists on Project Euler, consider '
                       'submitting a pull request to EulerPy on GitHub.')
            sys.exit(1)
