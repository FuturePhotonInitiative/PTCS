class UIController:
    def __init__(self, mainframe):
        self.mainframe = mainframe

    def rebuild_all_pages(self):
        self.rebuild_queue_page()
        self.rebuild_experiment_results_page()

    def rebuild_queue_page(self):
        self.mainframe.queue_page.reload()

    def rebuild_experiment_results_page(self):
        self.mainframe.experiment_results_page.reload()