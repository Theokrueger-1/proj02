import sys

#dictionary to match state + GUI event messages to new state and output messages. 
#Format (state, event message ) ->  (state, action message)
#We can use lookups 
TRANSITIONS = { 
    #Transitions from BASE state
    ("BASE", "clickTriChooseButton"): ("T_PANE_OPEN", ["showTP 0"]),
    ("BASE", "clickRecenterButton") : ("C_PANE_OPEN", ["showCP 0"]),
    ("BASE", "clickOnCanvas"):        ("BASE", ["moveC {data}"]),
    ("BASE", "mouseDownVertex"):      ("DRAGGING", ["selectV {data}"]),

    #Transittions from T_PANE_OPEN
    ("T_PANE_OPEN", "clickTriTypeChoice"): ("BASE", ["resetT {data}", "hideTP 0"]),
    ("T_PANE_OPEN", "click"):              ("BASE", ["hideTP 0"]), 
    ("T_PANE_OPEN", "clickOnCanvas"):      ("BASE", ["hideTP 0"]),

    #from C_PANE_OPEN
    ("C_PANE_OPEN", "recenterTextChange"): ("CHECK_CENTER", ["checkCT 0"]),
    ("C_PANE_OPEN", "click"):            ("BASE", ["hideCP 0"]), 
    ("C_PANE_OPEN", "clickOnCanvas"):    ("BASE", ["hideCP 0"]),

    #from CHECK_CENTER
    ("CHECK_CENTER", "recenterTextSucc"): ("BASE", ["moveC {data}", "hideCP 0"]),
    ("CHECK_CENTER", "recenterTextFail"): ("C_PANE_OPEN", ["errorCT 0"]),

    #from DRAGGING
    ("DRAGGING", "mouseMove"):        ("DRAGGING", ["moveV {data}"]),
    ("DRAGGING", "mouseUpCanvas"):    ("BASE", ["noop 0"]),
    ("DRAGGING", "mouseLeaveCanvas"): ("BASE", ["resetV 0"]),
} #treated the states as constants for naming convention, someone fact check me. 

if __name__ == "__main__":
    frgui = open("fromGUI","r")
    togui = open("toGUI","w")
    count = 0
    state = "BASE" #added variable to remember state

    while True:
        # Read event message
        try:
            msg, data = frgui.readline().split(maxsplit=1);
        except:
            break
        count += 1
        print(f'Read({count}): {msg} {data}',file=sys.stderr) #4DEBUG!

        
        #Loopup event message in transitions dictionary, then update state accordingly and print the action
        if (state, msg) in TRANSITIONS:
            state, actions = TRANSITIONS[(state, msg)] 
            for action in actions:
                response = action + data
                print(response + "\n",file=togui,flush=True)
                print(f'Sent({count}): {response}',file=sys.stderr) #4DEBUG!
        else:
            print("noop 0", file = togui, flush=TRUE)

## TODO Note 0: You MUST send to stderr an error message if you receive an event message that your transducer does not expect to see given the state you are in. The message should look like:
        #ERROR! Unexpected event message [eventMessage] while in state [i]