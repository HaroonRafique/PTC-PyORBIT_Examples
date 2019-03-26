import os

def suppress_STDOUT(callback):
        def function(name):
                null_fds = os.open(os.devnull, os.O_RDWR)
                save = os.dup(1)
                os.dup2(null_fds, 1)
                callback(name)
                os.dup2(save, 1)
                os.close(null_fds)
		os.close(save)
                return
        return function
