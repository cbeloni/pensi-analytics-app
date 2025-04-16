
class Progress:
    def __init__(self, progressBar):
        self.progress = 0
        self.progressBar = progressBar
        self.progressBar.setVisible(True)

    def set_progress(self, value):
        if not 0 <= value <= 100:
            raise ValueError("Progress value must be between 0 and 100.")
        
        self.progress = value
        self.progressBar.setValue(value)
        
        if value == 100:
            self.progressBar.setVisible(False)