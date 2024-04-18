f = open("C://Users/USER/Desktop/TransactionList.txt","a")
f.close()
import sys

def advert():
    print("              ####")
    print("         ##############")
    print("     #####   ## THE ##   #####")
    print("  ####### QUANTITY TRACKER ######")
    print(" ############ PROJECT ###########")
    print("     #####   #######   #####")
    print("         #############")
    print("              ####")
    print()
def midvert(tag):
    print("--------------------------------")
    print("--#####--{0}---####--".format(tag))
    print("--------------------------------")
def lowvert(tag):
    print("=================={0}=======================".format(tag))

def helper():
    lowvert("HELP SECTION")
    _extracted_from_helper_3("1. This program helps tracking the Quantity of things entered into it.\nIt can provide a list of all items, persons and order types (incoming and outgoing), all depending on user choices", "\n------- ABOUT INPUT ---------------", "2. For inputting choices, below is are two examples to allow the usability of this program:")

    _extracted_from_helper_6("\tExample 1:[1/mod]- modify contents; Your bracket choice->>\nThe input should be either: 1 or mod or modify. Regardless of what you wrote, these 3 examples of a typical input are valid.", "\tExample 2:[5/qt]- exit the program; Your bracket choice->>\nThe input can either be: 5 or qt or quitor exit. Same rule applies here.", "-------")

    print("3. Your input is made to be insensitive to sentence cases, i.e PencIl == Pencil == pencil == PENCIL.\nThis is to ensure errors are avoided in the recording of input/transaction parts.")
    print("4. Mistakes can be amended by choosing 'MODIFICATION'.\nHowever, it is wise to be keen when entering your data to minimize mistakes and allow fluency.")
    print()
    _extracted_from_helper_3("5. A Lot of work was put on the View Section mainly. The creator kept having many ideas and decided to write most of them.", "\n***WARNING!!!!!!!!!!!!!!!!!!!!!!!!***", "6. A DELETED ENTRY IS AN ENTRY GONE! IT CANNOT BE RECOVERED.")


# TODO Rename this here and in `helper`
def _extracted_from_helper_6(arg0, arg1, arg2):
    print(arg0)
    print(arg1)
    print(arg2)


# TODO Rename this here and in `helper`
def _extracted_from_helper_3(arg0, arg1, arg2):
    _extracted_from_helper_6(arg0, arg1, arg2)

def check_dic_key(dic, key):
    return 1 if key in dic else 0

def check_if_data_is_there(lists):
    if len(lists) == 0:
        print("No Entries Have Been Made!!->Back to Home<-")
        return 0
    return 1

advert()
#-----------Welcome information---------------------------
def welcome():
    lowvert("MAIN PAGE")
    #Data containers
    TransactionList = []
    all_items = {}
    all_persons = {}

    with open("C://Users/USER/Desktop/TransactionList.txt", "r") as Transtore:
        for line in Transtore:
            name, item, amount, in_ongoing = line.strip().split(",")
            lolist = [name, item, amount, in_ongoing]   #create inner list for a n by 4 list
            TransactionList.append(lolist)
            all_items[item] = all_items.get(item, 0) + int(amount)
            all_persons[name]  = all_persons.get(name, 0) + 1


    print("No. of Records: {0}. \tNo. of Items: {1}. \tNo. of Names: {2}".format(len(TransactionList), len(all_items), len(all_persons)))
    print("1.[Add]- Add Record\t2.[Vw]- View Record\t3.[Mod]- Modify Record \t4.[hp]- Help \t5.[Qt]- To Exit")
    print("----------")

    choice = input("Your Option->> ").lower()

    if choice in ['1',"add", "a"]:
        atranlist, add_item, add_person = iteminput()   #get lists of information from add function

        # add information to list
        with open("C://Users/USER/Desktop/TransactionList.txt", "a") as Transtore:
            for v in atranlist:
                TransactionList.append(list(v))
                v = ",".join(map(str, v)) + "\n"
                Transtore.writelines(v)

        #updating our information in our dictionaries
        for i in range(len(add_item)):
            a, b = add_item[i][0], int(add_item[i][1])
            all_items[a] = all_items.get(a, 0) + b

        for j in range(len(add_person)):
            a, b = add_person[j][0], int(add_person[j][1])
            all_persons[a] = all_persons.get(a, 0) + b

        welcome()

    elif choice in ['2',"vw", "view", "v"]:
        print("\n")
        view(TransactionList, all_items, all_persons)

    elif choice in ['3',"mod", "md", "modify"]:
        EditTransList = edit(TransactionList)       #gets new list from edit
        with open ("C://Users/USER/Desktop/TransactionList.txt","w") as Editranstore:
            #replace former details with new one
            for m in EditTransList:
                m = ",".join(map(str, m)) + "\n"        #write new information
                Editranstore.writelines(m)
        welcome()

    elif choice in ["4", "hp", "help"]:
        print("\n")
        helper()
        print("\n \n")
        welcome()

    elif choice in ['5',"qt", "quit", "exit"]: sys.exit()

    else:
        print("-->>> Invalid Entry!!! Main Page Again <<<--")
        welcome()

#transaction editing page
def iteminput():
    midvert("ADDING SECTION")

    Translist = []; add_item = []; add_person = []

    n = int(input("Number of items to add:->> "))
    print("Type Client_name, Item_name, Item_amount, (Incoming/Outgoing) separated by space.")

    for i in range(1, n+1):
        choice = input("**Item {0}:->> ".format(i)).strip().split()
        name = choice[0].strip().capitalize()
        itemname = choice[1].strip().capitalize()
        itemamount = choice[2].strip()
        recordtype = choice[3].strip().capitalize()

        #checks if input is plural, i.e with an s e.g books, pens
        laslen = len(itemname)
        if itemname[laslen-1] == "s":
            itemname = itemname[:-1] #remove the s, assuming its plural
        #check done

        Translist = Translist + [[name, itemname, itemamount, recordtype]]              #i.e ["Stormy", "Pencils", 26, "Incoming"]
        add_item = add_item + [[itemname, int(itemamount)]]                 #i.e ["Pencil", "26"]
        add_person = add_person + [[name, 1]]                                    #i.e ["Maguma", 1]
    print("----------")
    print("{0} items have been added! Exiting to Welcome Screen.\n".format(n))
    return Translist, add_item, add_person

#search/view page
def view(Transaction_List, all_items, all_persons):
    print("\n")
    midvert("VIEW SECTION")
    print("1.All Items Ever.\t2.All Clients Ever. \t3.Specific Record Type.")
    print("4.Recent Files.\t\t5.All Item History.\t6.Specific Item.")
    print("7.Specific Person.\t8.Direct Search.\t9.Home.")
    print("10.Exit/Quit the program.")
    print("----------")
    choice = input("**Your Input:->> ").lower()
    print("\n")

    #below are our view section choices
    if choice in ['1', 'allitems']:
        lowvert("All Items")
        view_all_items(Transaction_List, all_items,all_persons)

    elif choice in ["2", "allclients"]:
        lowvert("All Clients")
        view_all_persons(Transaction_List, all_items,all_persons)

    elif choice in ["3", "recordtype"]:
        lowvert("Record Type - Incoming/Outgoing")
        view_by_record_type(Transaction_List, all_items,all_persons)

    elif choice in ["4", "recentitems"]:
        lowvert("RECENT ITEMS")
        view_recent_items(Transaction_List, all_items, all_persons)

    elif choice in ["5","allhistory"]:
        lowvert("ALL TRANSACTIONS")
        view_all_item_history(Transaction_List, all_items, all_persons)

    elif choice in ["6", "specificitem"]:
        lowvert("SPECIFIC ITEM VIEW")
        view_specific_item(Transaction_List, all_items, all_persons)

    elif choice in ["7","specificperson"]:
        lowvert("SPECIFIC PERSON VIEW")
        view_specific_person(Transaction_List, all_items, all_persons)

    elif choice in ["8", "direct"]:
        lowvert("Direct Specific Search View")
        view_multiple_RecordType(Transaction_List, all_items, all_persons)

    elif choice in ["9", "home", "main"]:
        welcome()

    elif choice in ["10","quit", "exit"]:
        sys.exit()

    else:
        print("Invalid Entry!!!\n")
        view(Transaction_List, all_items, all_persons)

#----------------Viewing/Search Functions-----------
#They kind of act the same but with different functionalities

def view_specific_person(Transaction_List, all_items, all_persons):
    flag = check_if_data_is_there(Transaction_List)
    if flag == 0:
        welcome()

    choice = input("Name:->>").capitalize()
    len_people = len(all_persons)

    dic_flag = check_dic_key(all_persons, choice) #return 1 for true, 0 for false

    if dic_flag == 0:
        print("No entry for {0}\n".format(choice))
    else:
        print(f"{'No.':<4}{'--Name--': <15}{'--Item Name--': ^16}{'--Item Amount--':^20}{'--Type--':>2}")
        #no of entries the person made, numbering in order of first to last
        nocount = 0
        for i in range(len(Transaction_List)):
            if Transaction_List[i][0] == choice:
                nocount += 1
                print(f"{nocount:<4}{Transaction_List[i][0] : <15}{Transaction_List[i][1]: ^16}{Transaction_List[i][2] : >9}")
    print("----\n")
    view(Transaction_List, all_items, all_persons)  #return to view

def view_specific_item(Transaction_List, all_items,all_persons):

    flag = check_if_data_is_there(Transaction_List)
    if flag == 0:
        welcome()

    choice = input("Item name:->>").capitalize()

    #check if key exists
    dic_flag = check_dic_key(all_items, choice) #return 1 for true, 0 for false
    if dic_flag == 0:
        print("No Entry for {0}\n".format(choice))
    else:
        _extracted_from_view_specific_item_14(Transaction_List, choice)
    print("\n")
    view(Transaction_List, all_items, all_persons)  #return to view


# TODO Rename this here and in `view_specific_item`
def _extracted_from_view_specific_item_14(Transaction_List, choice):
    print(f"{'No.':<4}{'--Name--': <15}{'--Item Name--': ^16}{'--Item Amount--':^20}{'--Type--':>2}")
    itemcount = 0 #counts amount of item
    nocount = 0
    for i in range(len(Transaction_List)):
        if Transaction_List[i][1] == choice:
            nocount += 1 #for indexing from first position
            print(f"{nocount:<4}{Transaction_List[i][0] : <15}{Transaction_List[i][1] : ^16}{Transaction_List[i][2]: ^20}{Transaction_List[i][3] : >2}")
            itemcount += int(Transaction_List[i][2])
    print("------")
    print("Total Amount of: {0}s -> {1}\n".format(choice, itemcount))

#All items History Output
def view_all_item_history(Transaction_List, all_items, all_persons):

    flag = check_if_data_is_there(Transaction_List)
    if flag == 0:
        welcome()

    print(f"{'No.':<4}{'--Name--': <15}{'--Item Name--': ^16}{'--Item Amount--':^20}{'--Type--':>2}")

    for count, choice in enumerate(Transaction_List, start=1):
        print(f"{count:<3}->:{choice[0]: <15}{choice[1]: <16}{choice[2]: <9}{choice[3]: >9}")
    print("\n")
    view(Transaction_List, all_items, all_persons)  #return to view

#Recent items
def view_recent_items(Transaction_List, all_items, all_persons):

    flag = check_if_data_is_there(Transaction_List)
    if flag == 0:
        welcome()

    choice = int(input("View the last ___ items?->> "))
    len_total = len(Transaction_List)
    len_choice = len_total - choice
    #what if its greater than current length
    if len_choice <0:
        print("ERROR: NEGATIVE VALUE FOR RECENT ITEMS!! CURRENT TOTAL OF RECORD IS {0}".format(len_total))
    else:
        print(f"{'No.':<4}{'--Name--': <15}{'--Item Name--': ^16}{'--Item Amount--':^20}{'--Type--':>2}")
        for i in range(len_choice, len_total):
            print(f"{'->':<4}{Transaction_List[i][0] : <15}{Transaction_List[i][1] : ^16}{Transaction_List[i][2]: ^20}{Transaction_List[i][3] : >2}")
    view(Transaction_List, all_items, all_persons)  #return to view

#See all people
def view_all_persons(Transaction_List, all_items,all_persons):
    flag = check_if_data_is_there(Transaction_List)
    if flag == 0:
        welcome()

    print(f"{'No.':<4}{'Client Name':<15}")
    temporary_list = list(all_persons.keys())
    for nocount, temporary in enumerate(temporary_list, start=1):
        print(f"{nocount:<4}{temporary: <15}")
    print("------")
    print("\n")
    view(Transaction_List, all_items, all_persons)  #return to view

#see all items
def view_all_items(Transaction_List, all_items,all_persons):
    flag = check_if_data_is_there(Transaction_List)
    if flag == 0:
        welcome()

    print(f"{'No.':<4}{'Item Name':<15}")
    temporary_list = list(all_items.keys())
    for nocount, temporary in enumerate(temporary_list, start=1):
        print(f"{nocount:<4}{temporary: <15}")
    print("------")
    print("\n")
    view(Transaction_List, all_items, all_persons)  #return to view

#Record Type Looping Choice
def view_recordtype_loop_save(Transaction_List, recordtype):

    flag = check_if_data_is_there(Transaction_List)
    if flag == 0:
        welcome()

    print(f"{'No.':<4}{'--Name--': <15}{'--Item Name--': ^16}{'--Item Amount--':^20}{'--Type--':>2}")
    nocount = 0
    for i in range(len(Transaction_List)):
        if Transaction_List[i][3] == recordtype.capitalize():
            nocount += 1
            print(f"{nocount:<4}{Transaction_List[i][0] : <15}{Transaction_List[i][1] : ^16}{Transaction_List[i][2]: ^20}{Transaction_List[i][3] : >2}")
    print("--****Number of desired records: {0}".format(nocount))

#view by record type
def view_by_record_type(Transaction_List, all_items, all_persons):
    flag = check_if_data_is_there(Transaction_List)
    if flag == 0:
        welcome()

    choice = input("**Incoming/Outgoing? Your Input:->>").strip().lower()
    print("-----")
    if choice in ["in", "incoming"]:
        choice = "incoming"
        view_recordtype_loop_save(Transaction_List, choice)

    elif choice in ["out", "outgoing"]:
        choice = "outgoing"
        view_recordtype_loop_save(Transaction_List, choice)

    else:
        print("ERROR: INVALID INPUT!!!")
    print("\n")

    view(Transaction_List, all_items, all_persons)  #return to view

#see all records according to type
def view_multiple_RecordType(Transaction_List, all_items, all_persons):

    flag = check_if_data_is_there(Transaction_List)
    if flag == 0:
        welcome()

    print("Example->> Incoming client wingo or:->> outgoing item pencil")
    print("Separate input with a space:->> <record_type> <client/item> <client_name/item_name>")
    choice = input("Your Input:->>").strip().split()
    print("------")


    if choice[1].lower() in [1, 'client', 'person']:
        view_check_multiple_record(Transaction_List, list(all_persons.keys()), choice[0], choice[1], choice[2])

    elif choice[1].lower() in [2, "item", "tool"]:
        view_check_multiple_record(Transaction_List, list(all_items.keys()), choice[0], choice[1], choice[2])

    else:
        print("INVALID INPUT!!!")
    print("\n")
    view(Transaction_List, all_items, all_persons)  #return to view

def view_check_multiple_record(Transaction_List, ItemClientCol, RecordType, InforType,  ItemClientName):
    xxx = 0 if InforType.lower() in ['client', 'person'] else 1
    flag = check_dic_key(ItemClientCol, ItemClientName.capitalize())
    if flag == 0:
        print("No Entry For {0}".format(ItemClientName.capitalize()))
    else:
        #check if it has the required record type, print what is there
        nocount = 0 #track if there is anything
        print(f"{'No.':<4}{'--Name--':<15}{'--Item Name--':^16}{'--Amount--':^20}")

        for i in range(len(Transaction_List)):
            if (Transaction_List[i][xxx].capitalize() == ItemClientName.capitalize()) and (Transaction_List[i][3].capitalize() == RecordType.capitalize()):
                nocount += 1
                print(f"{nocount:<4}{Transaction_List[i][0]:<15}{Transaction_List[i][1]:^16}{Transaction_List[i][2]:^20}")

        if nocount == 0:
            print("---")
            print("***:{0} Does Not Have Record Type: {1}".format(ItemClientName.upper(), RecordType.upper()))

#Transaction Modification
def edit(Transaction_List):

    flag = check_if_data_is_there(Transaction_List)
    if flag == 0:
        welcome()

    midvert("MODIFICATION SECTION")
    print(f"{'No.':<4}{'--Name--': <15}{'--Item Name--': ^16}{'--Item Amount--':^20}{'--Type--':>2}")

    for count, choice in enumerate(Transaction_List, start=1):
        print(f"{count:<3}->:{choice[0]: <15}{choice[1]: <16}{choice[2]: <9}{choice[3]: >9}")

    print("----------------------")
    print("What is it you want to edit?\n1.Name\t2.Item Name\t3.Item Amount\t3.Order Type\t5.Delete.\t6.Home")

    choice = input("**Your Option:-> ")
    choiceitem = int(input("Order Number?? :--> ")) - 1
    print("--------")

    edititemchoice = Transaction_List[choiceitem]

    s = " ".join(map(str, edititemchoice))

    print("*****Editing:->> {0}:| {1}".format(choiceitem + 1, s))

    if choice in ['1',"name"]:
        new_name = input("Old Name: {0}. New Name:->> ".format(Transaction_List[choiceitem][0])).strip().capitalize()
        Transaction_List[choiceitem][0] = new_name

    elif choice in ['2',"itemname"]:
        new_item_name = input("Old Item Name: {0}. New Item Name:->> ".format(Transaction_List[choiceitem][1])).strip().capitalize()
        Transaction_List[choiceitem][1] = new_item_name

    elif choice in ['3',"itemamount"]:
        new_item_amount = input("Old Amount: {0}. New Amount:->> ".format(Transaction_List[choiceitem][2])).strip()
        Transaction_List[choiceitem][2] = new_item_amount

    elif choice in ['4',"ordertype"]:
        new_order_type = input("Old Order Type: {0}. New Order Type:->> ".format(Transaction_List[choiceitem][3])).strip()
        Transaction_List[choiceitem][3] = new_order_type

    elif choice in ['5',"delete"]:
        print("Deleting Entry:-> {0}".format(*Transaction_List[choiceitem]))
        del(Transaction_List[choiceitem])

    elif choice in ["6","home"]:
        welcome()
    else:
        print("ERROR: INVALID ENTRY!!!")
        edit(Transaction_List)
    return Transaction_List

welcome()