def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
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
    def __init__(self, skip=10):
        self.progresses = {}
        self.skip = skip
        self.counter = 0

        self.finished = False

    def update_progress(self, name, value):
        if value == 100 and self.progresses[name] != 100:
            print(f"{name[0:40]} has finished downloading.")

        self.progresses[name] = value

        if not self.finished and self.counter % self.skip != 0:
            self.print_progress()
        self.counter += 1

    def print_progress(self):
        percentage = 0
        for name, progress in self.progresses.items():
            percentage += progress

        percentage = percentage / len(self.progresses)

        printProgressBar(percentage, 100, length=50,
                         printEnd="\r", prefix="Total:")
