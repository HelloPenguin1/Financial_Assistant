

def route_decision(state):
    """Return the workflow to visit next after vectorDB is constructed"""
    if state["intent"] == 'full_report':
        return "constructdb"
    elif state["intent"] == 'specific':
        return "retriever"
    else:
        return "Comparison_Agent"