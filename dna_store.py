import argparse;
import csv;

parser = argparse.ArgumentParser(description='Do huffman encoding.')
parser.add_argument('-d', action="store_true",
                    help='specifies that the programm will run on decryption mode');
parser.add_argument('file1', metavar='file1',
                    help='On encoding mode, file to be encrypted on decoding mode file to be decoded');
parser.add_argument('file2',metavar='file2',
                    help='On encoding mode,  encrypted file on decoding mode, decoded file');
parser.add_argument('file3',metavar='file3',
                    help='encryption array to be created or to be used');

args = parser.parse_args();

class node:

    frequency = 0;
    value = '';
    children = None;
    father = None;
    number = None;
    id = None;

    def __init__(self,frequency, value, children):

        self.frequency = frequency;
        self.value = value;
        self.children = children;

    def setId(self, id):
        self.id = id;

    def getId(self):
        return id;

    def setNum(self, num):
        self.number = num;

    def getNum(self):
        return self.number;

    def setFather(self, father):
        self.father = father;

    def getFather(self):
        return self.father;

    def setChildren(self,children):
        self.children = children;

    def getChildren(self):
        return self.children;

    def getValue(self):
        return self.value;

    def getFreq(self):
        return self.frequency;

    def toString(self):

        print("Value:" , self.getValue()
        , " Frequency:" , self.getFreq(),
        "Number" , self.getNum(), "Id", self.id);


class lettr:

    ltr = '';
    numbers = None;
    sn = None;

    def __init__(self, l):
        self.ltr = l;

    def setLetter(self, l):
        self.ltr = l;

    def getLetter(self):
        return self.ltr;

    def setNumbers(self, numbers):
        self.numbers = numbers;

    def getNumbers(self):
        return self.numbers;

    def setSNum(self, sn):
        self.sn = sn;

    def getSNum(self):
        return self.sn;


def exists(letter, array):

    for index  in range(len(array)):
        if(letter == array[index]):
            return index;
    return -1;

def sortByFreq(frequency, value):

    length = len(frequency);

    for i in range(length-1, -1, -1):

        for j in range( length-1, i-1, -1):

            if frequency[i] > frequency[j]:

                tempFreq = frequency[i];
                frequency[i] = frequency[j];
                frequency[j] = tempFreq;

                tempValue = value[i];
                value[i] = value[j];
                value[j] = tempValue;

def sortQueue(list):

    length = len(list)
    for i in range (length - 1, -1, -1):

        for j in range(length - 1, i-1, -1):

            if list[i].getFreq() > list[j].getFreq():

                tempNode = list[i];
                list[i] = list[j];
                list[j] = tempNode;



def encode():
    file = open(args.file1, 'r');

    text = file.read();

    Dna = [
            [-1, 0, 1 ,2],
            [2, -1, 0, 1],
            [1,	2, -1, 0],
            [0, 1, 2, -1]
    ]
    dnaletters = ['A','C','G','T'];

    frequency = [];
    value = [];

    for letter in text:

        index = exists(letter, value);

        if  index > 0:
            frequency[index] = frequency[index] + 1;
        else:
            value.append(letter);
            frequency.append(1);

    sortByFreq(frequency,value);
    start = 0;
    end = 3;
    fathers = [];
    flag = False;
    length = len(value);


    queue = [];
    secondqueue = [];

    for i in range(length):
        queue.append(node(frequency[i], value[i], None));



    sortQueue(queue);
    for q in queue:
        length = len(queue);

    counter = 0;
    while length > 1:

        totalFreq = 0;
        children  = [];

        if end > len(queue):
            end = len(queue);

        for i in range(start,end):
            totalFreq = totalFreq + queue[i].getFreq();
            children.append(queue[i]);

        father = node(totalFreq, None, None);

        j = 0;
        for child in children:
            queue.remove(child);
            child.setFather(father);
            child.setNum(j);
            child.setId(counter);
            secondqueue.append(child);
            j = j +1;
            counter = counter + 1;

        father.setChildren(children);
        queue.append(father);
        sortQueue(queue);

        length = len(queue);

    '''End of loop'''
    children = [];
    totalFreq = 0;
    for i in queue:
        totalFreq = totalFreq + i.getFreq();
        children.append(i);

    root = node(totalFreq, None, None);
    j = 0;
    for child in children:
        child.setFather(root);
        child.setNum(j);
        child.setId(counter);
        j = j +1;
        counter = counter + 1;

    father.setChildren(children);
    print("created priority queue, number of nodes:");

    print(len(secondqueue));

    letters = [];
    for index in range(len(secondqueue)):
        flag = False;
        num = [];
        father = secondqueue[index];
        if secondqueue[index].getValue() <> None:
            val = secondqueue[index].getValue();
            ltr = lettr(val);
            flag = True;
        while father <> None:
            if flag and father.getNum() <> None:
                num.append(father.getNum());
            father = father.getFather();
        if flag:
            ltr.setNumbers(num);
            letters.append(ltr);

    huffman = [];
    for l in text:
        for i in letters:
            if i.getLetter() == l:
                for j in i.getNumbers():
                    huffman.append(j);
    print("huffman encoding successfull");
    print("huffman: " + str(huffman));

    dnacoding = [];
    prev = 'A';
    for h in huffman:
        i = dnaletters.index(prev);
        prev = dnaletters[Dna[i].index(h)];
        dnacoding.append(prev);

    f = open(args.file2,'w');
    for d in dnacoding:
        f.write(d);
    print("writing dna successfull");

    with open(args.file3, 'w') as csvfile:
        fieldnames = ['letter', 'code']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for l in letters:
            cd = '';
            lt = l.getLetter();

            for i in l.getNumbers():
                cd = cd + str(i);

            writer.writerow({'letter': lt, 'code': cd});
    print("Writing cvs successfull");

def decode():

    Dna = [
            [-1, 0, 1 ,2],
            [2, -1, 0, 1],
            [1,	2, -1, 0],
            [0, 1, 2, -1]
    ]
    dnaletters = ['A','C','G','T'];

    file = open(args.file1, 'r');

    text = file.read();

    huffman = [];
    prev = 'A';
    for l in text:
        i = dnaletters.index(prev);
        j = dnaletters.index(l);
        num = Dna[i][j];
        prev = l;
        huffman.append(num);

    print("huffman" + str(huffman));

    ltrs = [];
    with open(args.file3) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            l = lettr(row['letter']);
            l.setSNum(row['code']);
            ltrs.append(l);

    text = "";
    h = 0;
    while h < len(huffman):
        size = h+1;
        flag = True;
        while flag:
            code = '';
            for i in range(h, size):
                code = code + str(huffman[i]);
            for s in ltrs:
                if code == s.getSNum():
                    text = text + s.getLetter();
                    print("text found:"+ text);
                    flag = False;
                    h = size;
                    break;
            if size == len(huffman):
                break;
            size = size + 1;

    file = open(args.file2, 'w');

    text = file.write(text);

if args.d:
    decode();
else:
    encode();
