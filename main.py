import csv
from timeit import default_timer as timer
import random
import matplotlib.pyplot as plt


class NodeABR:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class NodeARN:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.red = True
        self.parent = None


class ABR:
    def __init__(self):
        self.root = None

    def setRoot(self, key):
        self.root = NodeABR(key)

    def getRoot(self):
        return self.root

    def height(self, currentNode):
        if currentNode is None:
            return 0
        else:
            return max(self.height(currentNode.left), self.height(currentNode.right)) + 1

    def insert(self, key):
        if self.root is None:
            self.setRoot(key)
        else:
            self.insertNode(self.root, key)

    def insertNode(self, currentNode, key):
        if key <= currentNode.key:
            if currentNode.left:
                self.insertNode(currentNode.left, key)
            else:
                currentNode.left = NodeABR(key)
        elif key > currentNode.key:
            if currentNode.right:
                self.insertNode(currentNode.right, key)
            else:
                currentNode.right = NodeABR(key)

    def find(self, key):
        return self.findNode(self.root, key)

    def findNode(self, currentNode, key):
        if currentNode is None:
            return False
        elif key == currentNode.key:
            return True
        elif key < currentNode.key:
            return self.findNode(currentNode.left, key)
        else:
            return self.findNode(currentNode.right, key)


class ARN:
    def __init__(self):
        self.nil = NodeARN(0)
        self.nil.red = False
        self.nil.left = None
        self.nil.right = None
        self.root = self.nil

    def getRoot(self):
        return self.root

    def height(self, currentNode):
        if currentNode is None:
            return 0
        else:
            return max(self.height(currentNode.left), self.height(currentNode.right)) + 1

    def fixInsert(self, z):
        while z.parent.red:
            if z.parent == z.parent.parent.right:
                y = z.parent.parent.left
                # uncle
                if y.red:
                    z.parent.red = False
                    y.red = False
                    z.parent.parent.red = True
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.rightRotate(z)
                    z.parent.red = False
                    z.parent.parent.red = True
                    self.leftRotate(z.parent.parent)
            else:
                y = z.parent.parent.right
                # uncle

                if y.red:
                    z.parent.red = False
                    y.red = False
                    z.parent.parent.red = True
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.leftRotate(z)
                    z.parent.red = False
                    z.parent.parent.red = True
                    self.rightRotate(z.parent.parent)
            if z == self.root:
                break
        self.root.red = False

    def leftRotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def rightRotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert(self, key):
        newNode = NodeARN(key)
        newNode.parent = None
        newNode.left = self.nil
        newNode.right = self.nil
        newNode.key = key
        newNode.red = True

        parentNode = None
        currentNode = self.root

        while currentNode != self.nil:
            parentNode = currentNode
            if newNode.key < currentNode.key:
                currentNode = currentNode.left
            else:
                currentNode = currentNode.right

        # cambiamento del campo padre
        newNode.parent = parentNode
        if parentNode is None:
            self.root = newNode
        elif newNode.key < parentNode.key:
            parentNode.left = newNode
        else:
            parentNode.right = newNode

        if newNode.parent == None:
            newNode.red = False
            return

        if newNode.parent.parent == None:
            return

        #fixup
        self.fixInsert(newNode)

    def find(self, key):
        return self.findNode(self.root, key)

    def findNode(self, currentNode, key):
        if currentNode is None:
            return False
        elif key == currentNode.key:
            return True
        elif key < currentNode.key:
            return self.findNode(currentNode.left, key)
        else:
            return self.findNode(currentNode.right, key)


def main():
    #graph subplots
    figure, axis = plt.subplots(2, 2)

    # ABR INSERT randomizzato
    tableIBRR = [['Elements inserted', 'Time passed']]
    elementsIBRR = []
    timePassedIBRR = []
    treeBRRand = ABR()
    startInsBR = timer()
    for i in range(0, 501):
        x = random.randint(0, 2000)
        treeBRRand.insert(x)
        if (i > 0) & (i % 50 == 0):
            endInsBR = timer()
            intervallo = round(endInsBR - startInsBR, 3)
            elementsIBRR.append(i)
            timePassedIBRR.append(intervallo)
            tableIBRR.append([i, intervallo])

    file = open('timeIBRR.csv', 'w+', newline='')
    with file:
        write = csv.writer(file)
        write.writerows(tableIBRR)

    # plot
    axis[0, 0].plot(elementsIBRR, timePassedIBRR, label='BT, height '+str(treeBRRand.height(treeBRRand.getRoot())))

    # ABR FIND randomizzato
    startFindBR = timer()
    tableFBRR = [['Elements found', 'Time passed']]
    elementsFBRR = []
    timePassedFBRR = []
    for i in range(0, 501):
        findBR = random.randint(0, 2000)
        treeBRRand.find(findBR)
        if (i > 0) & (i % 50 == 0):
            endFindBR = timer()
            intervallo = round(endFindBR - startFindBR, 3)
            elementsFBRR.append(i)
            timePassedFBRR.append(intervallo)
            tableFBRR.append([i, intervallo])

    file = open('timeFBRR.csv', 'w+', newline='')
    with file:
        write = csv.writer(file)
        write.writerows(tableFBRR)

    # plot
    axis[1, 0].plot(elementsFBRR, timePassedFBRR, label='BT, height '+str(treeBRRand.height(treeBRRand.getRoot())))

    # ABR INSERT in ordine crescente
    treeBR = ABR()
    tableIBRC = [['Elements inserted', 'Time passed']]
    elementsIBRC = []
    timePassedIBRC = []
    startInsBR = timer()
    for i in range(0, 501):
        treeBR.insert(i)
        if (i > 0) & (i % 50 == 0):
            endInsBR = timer()
            intervallo = round(endInsBR - startInsBR, 3)
            elementsIBRC.append(i)
            timePassedIBRC.append(intervallo)
            tableIBRC.append([i, intervallo])

    file = open('timeIBRC.csv', 'w+', newline='')
    with file:
        write = csv.writer(file)
        write.writerows(tableIBRC)

    # plot
    axis[0, 1].plot(elementsIBRC, timePassedIBRC, label='BT, height '+str(treeBR.height(treeBR.getRoot())))

    # ABR FIND in ordine crescente
    startFindBR = timer()
    tableFBRC = [['Elements found', 'Time passed']]
    elementsFBRC = []
    timePassedFBRC = []
    for i in range(0, 501):
        findBR = random.randint(0, 2000)
        treeBR.find(findBR)
        if (i > 0) & (i % 50 == 0):
            endFindBR = timer()
            intervallo = round(endFindBR - startFindBR, 3)
            elementsFBRC.append(i)
            timePassedFBRC.append(intervallo)
            tableFBRC.append([i, intervallo])

    file = open('timeFBRC.csv', 'w+', newline='')
    with file:
        write = csv.writer(file)
        write.writerows(tableFBRC)

    # plot
    axis[1, 1].plot(elementsFBRC, timePassedFBRC, label='BT, height '+str(treeBR.height(treeBR.getRoot())))

    # ARN INSERT randomizzato
    treeRNRand = ARN()
    tableIRNR = [['Elements inserted', 'Time passed']]
    elementsIRNR = []
    timePassedIRNR = []
    startInsRN = timer()
    for i in range(0, 501):
        x = random.randint(0, 2000)
        treeRNRand.insert(x)
        if (i > 0) & (i % 50 == 0):
            endInsRN = timer()
            intervallo = round(endInsRN - startInsRN, 3)
            elementsIRNR.append(i)
            timePassedIRNR.append(intervallo)
            tableIRNR.append([i, intervallo])

    file = open('timeIRNR.csv', 'w+', newline='')
    with file:
        write = csv.writer(file)
        write.writerows(tableIRNR)

    # plot
    axis[0, 0].plot(elementsIRNR, timePassedIRNR, label='RB, height '+str(treeRNRand.height(treeRNRand.getRoot())))
    axis[0, 0].set_title("Tree - Random Insert")
    axis[0, 0].legend()

    # ARN FIND randomizzato
    startFindRN = timer()
    tableFRNR = [['Elements found', 'Time passed']]
    elementsFRNR = []
    timePassedFRNR = []
    for i in range(0, 501):
        findRN = random.randint(0, 2000)
        treeRNRand.find(findRN)
        if (i > 0) & (i % 50 == 0):
            endFindRN = timer()
            intervallo = round(endFindRN - startFindRN, 3)
            elementsFRNR.append(i)
            timePassedFRNR.append(intervallo)
            tableFRNR.append([i, intervallo])

    file = open('timeFRNR.csv', 'w+', newline='')
    with file:
        write = csv.writer(file)
        write.writerows(tableFRNR)

    # plot
    axis[1, 0].plot(elementsFRNR, timePassedFRNR, label='RB, height '+str(treeRNRand.height(treeRNRand.getRoot())))
    axis[1, 0].set_title("Tree - Random Find")
    axis[1, 0].legend()

    # ARN INSERT in ordine crescente
    treeRN = ARN()
    tableIRNC = [['Elements inserted', 'Time passed']]
    elementsIRNC = []
    timePassedIRNC = []
    startInsRN = timer()
    for i in range(0, 501):
        treeRN.insert(i)
        if (i > 0) & (i % 50 == 0):
            endInsRN = timer()
            intervallo = round(endInsRN - startInsRN, 3)
            elementsIRNC.append(i)
            timePassedIRNC.append(intervallo)
            tableIRNC.append([i, intervallo])

    file = open('timeIRNC.csv', 'w+', newline='')
    with file:
        write = csv.writer(file)
        write.writerows(tableIRNC)

    # plot
    axis[0, 1].plot(elementsIRNC, timePassedIRNC, label='RB, height '+str(treeRN.height(treeRN.getRoot())))
    axis[0, 1].set_title("Tree - Ascending Insert")
    axis[0, 1].legend()

    # ARN FIND in ordine crescente
    startFindRN = timer()
    tableFRNC = [['Elements found', 'Time passed']]
    elementsFRNC = []
    timePassedFRNC = []
    for i in range(0, 501):
        findRN = random.randint(0, 2000)
        treeRN.find(findRN)
        if (i > 0) & (i % 50 == 0):
            endFindRN = timer()
            intervallo = round(endFindRN - startFindRN, 3)
            elementsFRNC.append(i)
            timePassedFRNC.append(intervallo)
            tableFRNC.append([i, intervallo])

    file = open('timeFRNC.csv', 'w+', newline='')
    with file:
        write = csv.writer(file)
        write.writerows(tableFRNC)

    # plot
    axis[1, 1].plot(elementsFRNC, timePassedFRNC, label='RB, height '+str(treeRN.height(treeRN.getRoot())))
    axis[1, 1].set_title("Tree - Ascending Find")
    axis[1, 1].legend()

    figure.tight_layout(pad=3.0)
    plt.savefig('ABR e ARN.png')


if __name__ == "__main__":
    main()
