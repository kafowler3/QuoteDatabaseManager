# Quotes Database
# Last updated 01/10/24
ver = 0.3

# A program to store and sort quotes with the following features:
# 1. Displays stored quotes
# 2. Displays quotes belonging to a certain speaker
# 3. Displays quotes with a certain tag attached
# 4. Imports new quotes from .txt file
# 5. Display all used names
# 6. Display all used tags
# 7. Clean formatting for long quotes
# 8. Ability to hide quotes using "hidden" tag
# 9. Automatic removal of duplicates
# 10. Output selected quotes to .txt file

import os

# Subclass that contains all of the relevant data on a quote
#-----------------------------------------------------------
class entry:
    def __init__(self, key, quote, person, tags=[]):
        self.key = key
        self.quote = quote
        self.person = person
        self.tags = tags
        self.hidden = False
    def __str__(self):
        if (self.hidden):
            return f"{self.key}. (Hidden)"
        return self.showHidden()
    
    # Only way to show quote if hidden = True
    #----------------------------------------
    def showHidden(self):
        output = f"{self.key}. \"{self.quote}\" ~{self.person}"
        if (len(self.tags) > 0):
            output += f" {self.tags}"
        if (len(output) > 100):
            i = output[:100].rfind(' ')
            formattedOutput = output[:i]
            j = i + 92
            while j < len(output):
                j = output[i:j].rfind(' ')
                formattedOutput += f"\n\t{output[i:j]}"
                i = j
                j += 92
            formattedOutput += f"\n\t{output[i:]}"
            output = formattedOutput
        return output
    
    # Allows records to be kept in order when one is deleted
    #-------------------------------------------------------
    def decrement(self):
        self.key -= 1

# Subclass used to track information about entries in database
#-------------------------------------------------------------
class tag:
    def __init__(self, title):
        self.title = title
        self.count = 1
    def __str__(self):
        return f"{self.title} ({self.count})"
    def increment(self):
        self.count += 1

# Loads quotes from file
#-----------------------
quotes = []
with open("quotesData.txt", "a+") as data:
    data.seek(0)
    key = 0
    for line in data:
        line = line.rstrip()
        limiter1 = line.find('|')
        quote = line[:limiter1]
        person = "blank"
        tags = []
        if (line.find('|', limiter1+1) != -1):
            limiter2 = line.find('|', limiter1+1)
            person = line[limiter1+1:limiter2]
            limiter1 = limiter2
            limiter2 = line.find('|', limiter1+1)
            while (limiter2 != -1):
                tags.append(line[limiter1+1:limiter2].lower())
                limiter1 = limiter2
                limiter2 = line.find('|', limiter1+1)
            tags.append(line[limiter1+1:].lower())
            tags.sort()    
        else:
            person = line[limiter1+1:]
        item = entry(key,quote,person,tags)
        for element in tags:
                if element == "hidden":
                    item.hidden = True
                    break
        quotes.append(item)
        key += 1

# Header formatting function
#--------------------
def header(main = False, array = quotes):
    os.system('cls')
    print(f"\n\t\t- Quotes Database v{ver} -")
    if (main):
        print(f"\t\t{len(array)} quotes loaded.")
    print()

# Gives options after displaying quotes
#--------------------------------------
def pause(displayed, array = quotes, output = False):
    print()
    if output:
        print("\tNote: changes will only be saved to output; no changes will be saved to database.")
    opt = input ("\tTo modify a quote, enter the corresponding number.\n\tOr press enter to continue or \"R\" to return: ").rstrip()
    if (opt.isdigit() and int(opt) < len(array)):
            modify(opt, displayed, array)
            header()
            for item in displayed:
                print(item)
            return pause(displayed, array, output)
    elif (opt == ""):
        return 1
    if (opt[0] == 'r' or opt[0] == 'R'):
        return -1
    return 1

# Modifies individual quote data
#-------------------------------
def modify(key, displayed, array = quotes):
    key = int(key)
    header()
    print(array[key])
    opt = input("\n\t1. Modify quote\n\t2. Modify name\n\t3. Modify tags\n\t4. Delete entry\n\t(Press \"R\" to return): ")
    if (opt == "" or (opt[0] =='r' or opt[0] == "R")):
        return -1
    header()
    print(array[key])

    # Modifies quote
    #---------------
    if (opt == '1'):
        array[key].quote = input("\n\tEnter replacement quote: ").rstrip()
    
    # Modifies name
    #--------------
    elif (opt == '2'):
        array[key].person = input("\n\tEnter replacement name: ").rstrip()
    
    # Modified tags
    #--------------
    elif (opt == '3'):
        newTags = []
        newTag = input("\n\tEnter replacement tag (leave blank if none): ").rstrip()
        while (newTag != ""):
            newTags.append(newTag)
            newTag = input("\tEnter a tag (leave blank if there are no more): ").rstrip().lower()
        newTags.sort()
        array[key].tags = newTags
        for element in newTags:
            if element == "hidden":
                array[key].hidden = True
                break
    
    # Deletes entry
    #--------------
    elif (opt == '4'):
        array.pop(key)
        for item in displayed:
            if item.key == key:
                displayed.remove(item)
        while (key < len(quotes)):
            array[key].decrement()
            key += 1
        return
    modify(key, displayed, array)

# Saves quotes to file
#---------------------
def save():

    # Removes duplicates
    #-------------------
    copies = quotes.copy()
    j = 0
    for item in quotes:
        i = j + 1 
        while i < len(copies):
            if (item.quote == copies[i].quote and item.person == copies[i].person):
                item.tags.extend(copies[i].tags)
                item.tags = set(item.tags)
                item.tags = list(item.tags)
                item.tags.sort()
                quotes.pop(i)
                copies.pop(i)
                k = i
                while k < len(copies):
                    quotes[k].decrement()
                    k += 1
            i += 1
        j += 1 

    # Saves data to file
    #-------------------
    with open("quotesData.txt", "w+") as data:
        for item in quotes:
            line = f"{item.quote}|{item.person}"
            for element in item.tags:
                line += f"|{element}"
            line += "\n"
            data.write(line)

# Main menu
#----------
opt = '1'
while(True):
    header(True)
    opt = input("\t1. Show all quotes\n\t2. Show quotes by name\n\t3. Show quotes by tag\n\t4. Show all names\n\t5. Show all tags\n\t6. Add quotes from .txt file\n\t7. Add quotes manually\n\t8. Export quotes as .txt file\n\t(Press \"Q\" to quit): ")
    if (opt != ""):
        opt = opt[0]
    if (opt == 'q' or opt =='Q'):
        break

    # Shows all quotes
    #-----------------
    if (opt == '1'):
        header()
        i = 0
        displayed = []
        while i < len(quotes):
            print(quotes[i])
            displayed.append(quotes[i])
            i += 1
            if (i % 20 == 0):
                opt = pause(displayed)
                if opt == -1:
                    break
                header()
                displayed.clear()
        if opt != -1:
            pause(displayed)         
    
    # Shows quotes by name
    #---------------------
    elif (opt == '2'):
        header()
        name = input("\tEnter name: ").rstrip()
        i = 0
        j = 0
        displayed = []
        while i < len(quotes):
            if (quotes[i].person == name):
                print(quotes[i])
                displayed.append(quotes[i])
                j += 1
                if (j % 20 == 0):
                    opt = pause(displayed)
                    if opt == -1:
                        break
                    header()
                    displayed.clear()
            i += 1
        if (j == 0):
            input(f"\tNo quotes found with name = {name}.\n\tPress enter to continue: ")
        elif (opt != -1):
            pause(displayed)
    
    # Shows quotes by tag
    #--------------------
    elif (opt == '3'):
        header()
        target = input("\tEnter tag: ").rstrip()
        i = 0
        j = 0
        displayed = []
        while i < len(quotes):
            for element in quotes[i].tags:
                if (element == target):
                    print(quotes[i].showHidden())
                    displayed.append(quotes[i])
                    j += 1
                    if (j % 20 == 0):
                        opt = pause(displayed)
                        if opt == -1:
                            break
                        header()
                        displayed.clear()
            i += 1
        if (j == 0):
            input(f"\tNo quotes found with name = {target}.\n\tPress enter to continue: ")
        elif (opt != -1):
            pause(displayed)

    # Shows all listed names
    #----------------------
    elif (opt == '4'):
        speakers = []
        for item in quotes:
            unique = True
            for speaker in speakers:
                if (item.person == speaker.title):
                    speaker.increment()
                    unique = False
                    break
            if (unique):
                speakers.append(tag(item.person))
        speakers.sort(key = lambda x: x.title)
        i = 0
        header()
        blank = True
        while i < len(speakers):
            if (i + 40 < len(speakers)):
                print(f"{str(speakers[i]).ljust(25)}\t\t{str(speakers[i+20]).ljust(25)}\t\t{speakers[i+40]}")
                blank = False
            elif (i + 20 < len(speakers)):
                print(f"{str(speakers[i]).ljust(25)}\t\t{speakers[i+20]}")
                blank = False
            else:
                print(speakers[i])
                blank = False
            i += 1
            if (i % 20 == 0):
                opt = input("\n\tPress enter to continue or \"R\" to return: ")
                if (opt != "" and (opt[0] == 'r' or opt[0] == "R")):
                    break
                header()
                i += 40
                blank = True
        if (not blank and opt != 'r' and opt != "R" and i >= len(speakers)):
            opt = input("\n\tPress enter to continue or \"R\" to return: ")

    # Shows all listed tags
    #---------------------
    elif (opt == '5'):
        #input("It made it here 1")
        attributes = [tag("*untagged*")]
        for item in quotes:
            if (item.tags == []):
                attributes[0].increment()
            else:
                for element in item.tags:
                    unique = True
                    for attribute in attributes:
                        if (element == attribute.title):
                            attribute.increment()
                            unique = False
                            break
                    if (unique):
                        attributes.append(tag(element))
        attributes[0].count -= 1
        if (attributes[0].count == 0):
            attributes.pop(0)
        attributes.sort(key = lambda x: x.title)
        i = 0
        header()
        blank = True
        while i < len(attributes):
            if (i + 40 < len(attributes)):
                print(f"{str(attributes[i]).ljust(25)}\t\t{str(attributes[i+20]).ljust(25)}\t\t{attributes[i+40]}")
                blank = False
            elif (i + 20 < len(attributes)):
                print(f"{str(attributes[i]).ljust(25)}\t\t{attributes[i+20]}")
                blank = False
            else:
                print(attributes[i])
                blank = False
            i += 1
            if (i % 20 == 0):
                opt = input("\n\tPress enter to continue or \"R\" to return: ")
                if (opt != "" and (opt[0] == 'r' or opt[0] == "R")):
                    break
                header()
                i += 40
                blank = True
        if (not blank and opt != 'r' and opt != "R" and i >= len(attributes)):
            opt = input("\n\tPress enter to continue or \"R\" to return: ")

    # Adds quotes from .txt file
    #---------------------------
    elif (opt == '6'):
        while(True):
            header()
            file = input("\tEnter file name (including .txt): ").rstrip()
            newQuotes = []
            with open(file, encoding="utf-8") as newData:
                newQuote = ""
                newPerson = ""
                for line in newData:
                    line = line.rstrip()
                    if (line != ""):
                        if line[0] == '"':
                            newQuote = line[1:]
                        elif line[0] == '-' or line[0] == '~':
                            newQuote = newQuote[:-1]
                            newPerson = line[1:].lstrip()
                            newKey = len(quotes) + len(newQuotes)
                            newQuotes.append(entry(newKey,newQuote,newPerson))
                        else:
                            newQuote += line
            def newQuotesOpt(opt):
                if (opt == 'r' or opt == 'R'):
                    return -1
                elif (opt == '1'):
                    header()
                    i = 0
                    displayed = []
                    while i < len(newQuotes):
                        print(newQuotes[i])
                        displayed.append(newQuotes[i])
                        i += 1
                        if (i % 20 == 0):
                            opt = pause(displayed, newQuotes)
                            if opt == -1:
                                break
                            header()
                            displayed.clear()
                    if opt != -1:
                        pause(displayed, newQuotes) 
                    header()
                    opt = input(f"\t{len(newQuotes)} quotes loaded from {file}.\n\n\t1. Show new quotes\n\t2. Save new quotes\n\t3. Discard new quotes\n\t(Enter \"R\" to return): ")
                    if (opt != ""):
                        opt = opt[0]
                    return newQuotesOpt(opt)
                elif (opt == '2'):
                    for item in newQuotes:
                        quotes.append(item)
                    return -1
                return 1   
            opt = input(f"\t{len(newQuotes)} quotes loaded from {file}.\n\n\t1. Show new quotes\n\t2. Save new quotes\n\t3. Discard new quotes\n\t(Enter \"R\" to return): ")
            if (opt != ""):
                opt = opt[0]
            opt = newQuotesOpt(opt)
            if (opt == -1):
                break

    # Adds quotes manually
    #---------------------
    elif (opt == '7'):
        newKey = len(quotes)
        while (True):
            header()
            newTags = []
            newQuote = input("\tEnter the quote: ").rstrip()
            newPerson = input("\tEnter the name attributed to the quote: ").rstrip()
            newTag = input("\tEnter a tag (leave blank if none): ").rstrip().lower()
            while (newTag != ""):
                newTags.append(newTag)
                newTag = input("\tEnter a tag (leave blank if there are no more): ").rstrip().lower()
            newTags.sort()
            newEntry = entry(newKey,newQuote,newPerson,newTags)
            header()
            print(newEntry)
            opt = input("\n\t1. Save quote\n\t2. Discard quote\n\t(Enter \"R\" to return): ")
            if (opt != ""):
                opt = opt[0]
            if (opt == '1'):
                quotes.append(entry(newKey,newQuote,newPerson,newTags))
                break
            if (opt == 'r' or opt == 'R'):
                break

    # Exports selected quotes to .txt file
    #-------------------------------------
    elif (opt == '8'):
        names = []
        flags = []
        for item in quotes:
            if item.person not in names:
                names.append(item.person)
            for attribute in item.tags:
                if attribute not in flags:
                    flags.append(attribute)
        selectedNames = []
        selectedFlags = []
        header()
        include = input("\tEnter a name to include (leave blank to include all names by default): ").strip()
        if (include == ""):
            selectedNames = names.copy()
            exclude = input("\tEnter a name to exclude (leave blank to exclude no names by default): ").strip()
            while (exclude != ""):
                if exclude in selectedNames:
                    selectedNames.remove(exclude)
                elif exclude not in names:
                    print(f"\t{exclude} is not a name in database.")
                exclude = input("\tEnter a name to exclude (leave blank to move to next step): ").strip()
        while (include != ""):
            if include in names:
                selectedNames.append(include)
            else:
                print(f"\t{include} is not a name in database.")
            include = input("\tEnter a name to include (leave blank to move to next step): ").strip()
        includeUntagged = False
        include = input("\tEnter a tag to include (leave blank to include all tags by default): ").strip()
        if (include == ""):
            selectedFlags = flags.copy()
            includeUntagged = True
            exclude = input("\tEnter a tag to exclude (leave blank to exclude no tags by default): ").strip()
            while (exclude != ""):
                exclude.lower()
                if exclude in selectedFlags:
                    selectedFlags.remove(exclude)
                elif exclude == "*untagged*":
                    includeUntagged = False
                else:
                    print(f"\t{exclude} is not a tag in database.")
                exclude = input("\tEnter a tag to exclude (leave blank to move to next step): ").strip()
            if "hidden" in selectedFlags:
                selectedFlags.remove("hidden")
        while (include != ""):
            include.lower()
            if include in flags:
                selectedFlags.append(include)
            elif include == "*untagged*":
                includeUntagged = True
            else:
                print(f"\t{include} is not a tag in database.")
            include = input("\tEnter a tag to include (leave blank to move to next step): ").strip()
        if not includeUntagged and len(selectedFlags) != 1:
            opt = input("\tOnly include quotes that have ALL desired tags (Y/N): ").strip()
        logicalAnd = False
        if opt != "" and (opt[0] == 'y' or opt[0] == 'Y'):
            logicalAnd = True
        selection = []
        for item in quotes:
            if item.person in selectedNames:
                if item.tags == [] and includeUntagged:
                    selection.append(item)
                elif logicalAnd:
                    belongs = True
                    for flag in selectedFlags:
                        if flag not in item.tags:
                            belongs = False
                            break
                    if belongs:
                        selection.append(item)
                else:
                    for attribute in item.tags:
                        if attribute in selectedFlags:
                            selection.append(item)
                            break
        if "hidden" not in selectedFlags:
            for select in selection:
                if "hidden" in select.tags:
                    selection.remove(select)
        while (True):
            header(True,selection)
            opt = input("\t1. Show selected quotes\n\t2. Overwrite file \"quotesOutput.txt\"\n\t3. Append to file \"quotesOutput.txt\"\n\t(Enter \"R\" to return): ").strip()
            if (opt != ""):
                opt = opt[0]
            if (opt == 'r' or opt == 'R'):
                break
            if (opt == '1'):
                header()
                i = 0
                displayed = []
                while i < len(selection):
                    print(selection[i].showHidden())
                    displayed.append(selection[i])
                    i += 1
                    if (i % 20 == 0):
                        opt = pause(displayed,selection,True)
                        if opt == -1:
                            break
                        header()
                        displayed.clear()
                if opt != -1:
                    pause(displayed,selection,True)
            elif (opt == "2"):
                with open("quotesOutput.txt", "w+", encoding="utf-8") as output:
                    for item in selection:
                        output.write(f"\"{item.quote}\"\n- {item.person}\n\n")
                input("\n\t\"quotesOutput.txt\" overwritten. Press enter to continue: ")
                break
            elif (opt == "3"):
                with open("quotesOutput.txt", "a+", encoding="utf-8") as output:
                    for item in selection:
                        output.write(f"\"{item.quote}\"\n- {item.person}\n\n")
                input("\n\t\"quotesOutput.txt\" appended. Press enter to continue: ")
                break
    save()