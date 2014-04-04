## OCR


Python OCR using OpenCV

### Commands:


    1. python -m generator.creator [-h] [-p PREFIX] [--dry-run]
    2. python -m generator.reader [-h] [-p PREFIX] [--dry-run] filename
    3. python generator.py [-h] [-p PREFIX] [--dry-run] [filename]
    4. ./test.sh [-h] [-lsd] [-p PATTERN] [filename [filename ...]]
    5. python dataset.py [-h] filename
    6. python ocr.py [-h] [-lsd] [-t TRAIN_RATIO] [-m MAX_PER_CLASS]


### 1. Create a dataset entry

    python -m generator.creator [-h] [-p PREFIX] [--dry-run]

**arguments:**
   
    -h, --help      Show help message and exit
    -p PREFIX, --prefix PREFIX
                    Add a prefix to the filename
    --dry-run       Run without writing files

This command open a blank image in which you can draw your letter / symbol / digit.  
When you have drawn your letter, press the corresponding key (`Shift` + `letter` works for majuscules)
to write the file `dataset/key/prefix-key.i.bmp`

* `Any Key` to write the file
* `DEL` to remove the last written file
* `SPACE` for reset
* `UP` to increase brush size
* `DOWN` to decrease brush size
* `ESC` to quit

**Example:**

    python -m generator.creator -p koeth_y
* Draw an `a`
* Press `a` key
* The file `dataset/a_small/koeth_y-a_small.0.bmp` is written
* Draw another char

----------------------------------------------

### 2. Read a scanned dataset

    python -m generator.reader [-h] [-p PREFIX] [--dry-run] filename

**arguments**:
	
    filename          The file to read
    -h, --help        Show help message and exit
    -p PREFIX, --prefix PREFIX
                      Add a prefix to the filenames
    --dry-run         Run without writing files

This command split a scanned dataset into multiple files.

* `SPACE` to write the dataset
* `UP` to increase boxes size
* `DOWN` to decrease boxes size

**Example:**

     python -m generator.reader scanned_dataset.bmp -p koeth_y
* Press `SPACE`

Output:
    
     Write dataset/a_small/koeth_y-a_small.1.bmp
     Write dataset/a/koeth_y-a.1.bmp
     Write dataset/b_small/koeth_y-b_small.1.bmp
     ...

----------------------------------------------

### 3. Dataset Generator

    python generator.py [-h] [-p PREFIX] [--dry-run] [filename]

**arguments:**
    
    filename          The file to read
    -h, --help        Show help message and exit
    -p PREFIX, --prefix PREFIX
                      Add a prefix to the filenames
    --dry-run         Run without writing files

If filename is provided execute generator.reader.

Otherwise execute generator.creator.

**Examples:**

    python generator.py -p koeth_y
    python generator.py 'scanned_dataset.bmp' -p koeth_y

----------------------------------------------

### 4. Test OCR

    ./test.sh [-h] [-lsd] [-p PATTERN] [filename [filename ...]]

**arguments:**

    filename      Image to recognize
    -h, --help    Show help message and exit
    -l            Recognize letters
    -s            Recognize symbols
    -d            Recognize digits
    -p PATTERN, --pattern PATTERN
                  Pattern to extract label from filename

If filenames are provided, recognize chars in filenames.

If pattern is provided, analyze the predictions.
   
`PATTERN` must be a command that extract the classification from the filename.
      
       > pattern.sh 'a_small.jpg'
       a
      
Otherwise, this command open a blank image in which you can draw your letter / symbol / digit.
When you press Space, the recognized char appears in a new window.

* `SPACE` to test
* `UP` to increase brush size
* `DOWN` to decrease brush size
* `r` for rest
* `ESC` for exit

**Examples:**

     ./test.sh -ld `ls dataset/*/*.bmp` -p test/pattern.sh
     ./test.sh -d
     ./test.sh -l foo.png
     ./test.sh -lsd -p test/pattern.sh bar.bmp foo.png

----------------------------------------------
   
### 5. Display OCR pre-processing

    python dataset.py [-h] filename

**arguments:**
	
    filename      File to pre-process
    -h, --help    show help message and exit

**Example:**

     python dataset.py letter.bmp

----------------------------------------------

### 6. Train model

    python ocr.py [-h] [-lsd] [-t TRAIN_RATIO] [-m MAX_PER_CLASS]

**arguments:**

    -h, --help      show this help message and exit
    -l              Train to recognize letters
    -s              Train to recognize symbols
    -d              Train to recognize digits
    -t TRAIN_RATIO, --train-ratio TRAIN_RATIO
    -m MAX_PER_CLASS, --max-per-class MAX_PER_CLASS
    
`TRAIN_RATIO` [0.0-1.0] is the ratio between training and test samples (1 = 0 test samples).

`MAX_PER_CLASS` is the maximum samples (training + test) allowed per class.

**Example:**

     python ocr.py -lsd -t 0.5 -m 50
