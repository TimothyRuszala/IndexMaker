# IndexMaker
A good friend was translating Ovid's Metamorphoses, and I wrote this small Python program to help him compile an index of names. With two basic commands, this program allows the user to automatically add and remove names from a generated index.txt file.

**Unfortunately, due to copyright I cannot include an example of the text from which the index is created.**

But feel free to adapt this code for your own purposes!


## Usage

Names can be searched from the command line.

For example, to add all instances of 'Jove' to the index, type:
```
python3 MetIndex.py Jove
```
To remove the entry for 'Jove' from the index:
```
python3 MetIndex.py -rm Jove # removes the entry for 'Jove' from the index
```

