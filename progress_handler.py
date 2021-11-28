def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    Args:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """

    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


class ProgressHandler:
    """Handles progresses of tasks, prints the loading bar on the console."""

    def __init__(self, skip=10):
        self.progresses = {}
        self.skip = skip
        self.counter = 0

        self.finished = False

    def update_progress(self, name, value):
        """Update the progress of a task. Triggers the console load printing.

        Args:
            name (str): name of the task. 
            value (int): progress's value, [0, 100].
        """

        if value == 100 and self.progresses[name] != 100:
            print(f"{name[0:40]} has finished downloading.")
            self.finished = True

        self.progresses[name] = value

        if not self.finished and self.counter % self.skip != 0:
            self.print_progress()
        self.counter += 1

    def print_progress(self):
        """Print the progress in the console."""

        percentage = 0
        for progress in self.progresses.values():
            percentage += progress

        percentage = percentage / len(self.progresses)

        printProgressBar(percentage, 100, length=50,
                         printEnd="\r", prefix="Total:")
