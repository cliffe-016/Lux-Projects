def analyze(filename):
    # Read the file and handle the errors gracefullt
    try:    
        with open(filename, "r") as file:
            text = file.read()
            #Count the characters
            char_count = len(text)
            print("Total characters: ", char_count)
            
            #Count the words
            words = text.split()
            word_count = len(words)
            print("Total words: ", word_count)

            #Count line
            lines = text.splitlines()
            line_count = len(lines)
            print("Total lines: ", line_count)
            
            #Create dictionary to store words and theircounts
            word_ct = {}

            #count the words and tally the result
            for word in words:
                word = word.lower() # stamdardize the words
                if word in word_ct:
                    word_ct[word] += 1
                else:
                    word_ct[word] = 1

            # initialize empty key, value
            most_common = None     #key
            highest_count = 0   #value

            # Iterate through the dictionary and find the most ocmmon ord
            for word, count in word_ct.items():
                if count > highest_count:
                    most_common = word
                    highest_count = count 
            print("Most common word: ", most_common)

    except FileNotFoundError:
        print("Error: file not found")

if __name__ == "__main__":
    analyze("file.txt")
