import torch
import os

class SaveModelCallback:
    def __init__(self, freq, model, path, monitor="val_loss", term=None, term_value=None, save_all=False):
        self.freq = freq
        self.model = model
        self.path = path
        self.epoch = 0
        self.min_loss = float("inf")
        self.monitor = monitor
        self.term = term
        self.term_value = term_value
        self.save_all = save_all

    def on_epoch_end(self, epoch, logs):
        self.epoch += 1
        current_loss = logs.get(self.monitor)

        print(f"Epoch {self.epoch}: current {self.monitor} = {current_loss}, best = {self.min_loss}")
        save = False

        if (self.epoch % self.freq == 0) and (current_loss < self.min_loss):
            if (self.term is not None and self.term_value is not None) or self.save_all:
                if (logs.get(self.term, 0) > self.term_value) or self.save_all:
                    save = True
            else:
                save = True

            if save:
                print(f"Saving model to {self.path}...")
                torch.save(self.model.state_dict(), self.path)
                self.min_loss = current_loss
                print("Model saved.")
