# Testdatei für flake8

def boo():
    x=1     # Leerzeichen-Fehler
    if x == 1:
        if True:
            if True:
                if True:
                    if True:
                        if True:
                            if True:
                                print("Zu tief verschachtelt!")  # zu komplex

def fuz(): print("Das ist eine zu lange Zeile mit über 79 Zeichen,  flake8 sich sicher darüber beschweren :)")  # zu lange Zeile

