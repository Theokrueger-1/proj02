import sys

#dictionary to match state + GUI event messages to new state and output messages. 
#Format (state, event message ) ->  (state, action message)
#We can use lookups 
TRANSITIONS = {
    #Transitions from INIT state
    ("INIT", "documentReady"): ("BASE", ["noop 0"]),

    #Transitions from BASE state
    ("BASE", "clickTriChooseButton"): ("T_PANE_OPEN", ["showTP 0"]),
    ("BASE", "clickRecenterButton"): ("C_PANE_OPEN", ["showCP 0"]),
    ("BASE", "mouseDownVertex"): ("DRAGGING", ["selectV {data}"]),

    #Possible No-Ops in BASE
    ("BASE", "click"): ("BASE", ["noop 0"]),
    ("BASE", "clickOnCanvas"): ("BASE", ["noop 0"]),
    ("BASE", "mouseMove"): ("BASE", ["noop 0"]),
    ("BASE", "mouseUpCanvas"): ("BASE", ["noop 0"]),
    ("BASE", "mouseLeaveCanvas"): ("BASE", ["noop 0"]),

    #Transitions from T_PANE_OPEN
    ("T_PANE_OPEN", "clickTriTypeChoice"): ("BASE", ["resetT {data}", "hideTP 0"]),
    ("T_PANE_OPEN", "clickTriChooseButton"): ("BASE", ["hideTP 0"]),
    ("T_PANE_OPEN", "clickRecenterButton"): ("C_PANE_OPEN", ["hideTP 0", "showCP 0"]),
    ("T_PANE_OPEN", "click"): ("BASE", ["hideTP 0"]),
    ("T_PANE_OPEN", "clickOnCanvas"): ("BASE", ["hideTP 0"]),

    #Possible No-Ops in T_PANE_OPEN
    ("T_PANE_OPEN", "mouseMove"): ("T_PANE_OPEN", ["noop 0"]),
    ("T_PANE_OPEN", "mouseUpCanvas"): ("T_PANE_OPEN", ["noop 0"]),
    ("T_PANE_OPEN", "mouseLeaveCanvas"): ("T_PANE_OPEN", ["noop 0"]),
    ("T_PANE_OPEN", "mouseDownVertex"): ("T_PANE_OPEN", ["noop 0"]),

    #Transitions from C_PANE_OPEN
    ("C_PANE_OPEN", "recenterTextChange"): ("CHECK_CENTER", ["checkCT {data}"]),
    ("C_PANE_OPEN", "clickOnCanvas"): ("BASE", ["moveC {data}", "hideCP 0"]),
    ("C_PANE_OPEN", "clickRecenterButton"): ("BASE", ["hideCP 0"]),
    ("C_PANE_OPEN", "clickTriChooseButton"): ("T_PANE_OPEN", ["hideCP 0", "showTP 0"]),
    ("C_PANE_OPEN", "click"): ("BASE", ["hideCP 0"]),

    #Possible No-Ops in C_PANE_OPEN
    ("C_PANE_OPEN", "clickRecenterPane"): ("C_PANE_OPEN", ["noop 0"]),
    ("C_PANE_OPEN", "clickRecenterTextBox"): ("C_PANE_OPEN", ["noop 0"]),
    ("C_PANE_OPEN", "mouseMove"): ("C_PANE_OPEN", ["noop 0"]),
    ("C_PANE_OPEN", "mouseUpCanvas"): ("C_PANE_OPEN", ["noop 0"]),
    ("C_PANE_OPEN", "mouseLeaveCanvas"): ("C_PANE_OPEN", ["noop 0"]),
    ("C_PANE_OPEN", "mouseDownVertex"): ("C_PANE_OPEN", ["noop 0"]),

    #Transitions from CHECK_CENTER
    ("CHECK_CENTER", "recenterTextSucc"): ("BASE", ["moveC {data}", "hideCP 0"]),
    ("CHECK_CENTER", "recenterTextFail"): ("C_PANE_OPEN", ["errorCT 0"]),

    #Possible No-Ops in CHECK_CENTER
    ("CHECK_CENTER", "mouseMove"): ("CHECK_CENTER", ["noop 0"]),
    ("CHECK_CENTER", "mouseLeaveCanvas"): ("CHECK_CENTER", ["noop 0"]),
    ("CHECK_CENTER", "clickRecenterPane"): ("CHECK_CENTER", ["noop 0"]),
    ("CHECK_CENTER", "clickRecenterTextBox"): ("CHECK_CENTER", ["noop 0"]),

    #Transitions from DRAGGING
    ("DRAGGING", "mouseMove"): ("DRAGGING", ["moveV {data}"]),
    ("DRAGGING", "mouseUpCanvas"): ("BASE", ["noop 0"]),
    ("DRAGGING", "mouseLeaveCanvas"): ("BASE", ["resetV 0"]),
}

if __name__ == "__main__":
    frgui = open("fromGUI","r")
    togui = open("toGUI","w")
    count = 0
    state = "INIT" #added variable to remember state

    while True:
        # Read event message
        try:
            msg, inData = frgui.readline().strip().split(maxsplit=1); #strip the input of \n
        except:
            break
        count += 1

        
        #Loopup event message in transitions dictionary, then update state accordingly and print the action
        if (state, msg) in TRANSITIONS:
            state, actions = TRANSITIONS[(state, msg)] 
            for action in actions:
                response = action.format(data=inData) #replace the format placeholder {data} with input data
                print(response,file=togui,flush=True)
        else:
            print(f"ERROR! Unexpected event message [{msg}] while in state [{state}]", file=sys.stderr)
            print("noop 0", file = togui, flush=True)

