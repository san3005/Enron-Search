#!/usr/bin/env python3
# imports
import os
import mailbox
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: enron_search <search type> <search term>")
        sys.exit(1)
    
    search_type = sys.argv[1].lower()
    if search_type == "term_search":
        # for term_search we need at least 3 arguments
        if len(sys.argv) < 3:
            print("Usage: enron_search term_search <search term1> <search term2> ... <search termN>")
            sys.exit(1)
        # get the search terms - remove duplicates and convert to a list of lower case strings
        search_terms = list(set(map(lambda term: term.lower() , sys.argv[2:])))
        # number of matches
        matches = 0
        # iterate through all the mbox files under "enron"
        for file in os.listdir("enron"):
            mbox = mailbox.mbox("enron/" + file)
            # iterate through all messages in the mbox file
            for message in mbox:
                # get the message body
                body = message.get_payload()
                # check if all the search terms are present in the message body
                if all(map(lambda term: term in body, search_terms)):
                    matches += 1
                    # print the counter, from address and date
                    print("{}. {} {}".format(matches, message["From"], message["Date"]))
        # print the total number of matches
        print("Results found: {}".format(matches))                    
    elif search_type == "address_search":
        # last_name and first_name are required for address_search
        if len(sys.argv) != 4:
            print("Usage: enron_search address_search <last name> <first name>")
            sys.exit(1)
        # get the last name and first name
        last_name = sys.argv[2].lower()
        first_name = sys.argv[3].lower()
        # number of matches
        matches = 0
        # iterate through all the mbox files under "enron"
        for file in os.listdir("enron"):
            mbox = mailbox.mbox("enron/" + file)
            # iterate through all messages in the mbox file
            for message in mbox:
                # check if the message is sent/received by the given person
                msg_from, msg_to = message["From"], message["To"]
                msg_from = str(msg_from).lower() if msg_from != None else ""
                msg_to = str(msg_to).lower() if msg_to != None else ""
                if last_name in msg_from and first_name in msg_from:
                    matches += 1
                    # print <counter>. <from address> to <to address> on <date>
                    print("{}. {} to {} on {}".format(matches, message["From"], message["To"], message["Date"]))
                elif last_name in msg_to and first_name in msg_to:
                    matches += 1
                    # print <counter>. <from address> to <to address> on <date>
                    print("{}. {} to {} on {}".format(matches, message["From"], message["To"], message["Date"]))
        # print the total number of matches
        print("Results found: {}".format(matches))
    elif search_type == "interaction_search":
        # address1 and address2 are required for interaction_search
        if len(sys.argv) != 4:
            print("Usage: enron_search interaction_search <address1> <address2>")
            sys.exit(1)
        # get the addresses
        address1 = sys.argv[2].lower()
        address2 = sys.argv[3].lower()
        # number of matches
        matches = 0
        # iterate through all the mbox files under "enron"
        for file in os.listdir("enron"):
            mbox = mailbox.mbox("enron/" + file)
            # iterate through all messages in the mbox file
            for message in mbox:
                # check if the message is sent/received by the given person
                msg_from, msg_to = message["From"], message["To"]
                msg_from = str(msg_from).lower() if msg_from != None else ""
                msg_to = str(msg_to).lower() if msg_to != None else ""
                if address1 in msg_from and address2 in msg_to:
                    matches += 1
                    print("{}. {} -> {} [Subject: {}] {}".format(matches, message["From"], message["To"], message["Subject"], message["Date"]))
                elif address2 in msg_from and address1 in msg_to:
                    matches += 1
                    print("{}. {} -> {} [Subject: {}] {}".format(matches, message["From"], message["To"], message["Subject"], message["Date"]))
        # print the total number of matches
        print("Results found: {}".format(matches))
    else:
        print("Invalid search type. Please choose from term_search, address_search, or interaction_search")
        sys.exit(1)

