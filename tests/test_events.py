from sentinelrisk.nlp.event_classifier import classify_event

def test_event_classification():
    assert classify_event("Central bank signals an interest rate hike")[0] == "macroeconomic"
    assert classify_event("Company warns of a credit loss and possible default")[0] == "credit_event"
    assert classify_event("Unexpected geopolitical attack and new sanctions")[0] == "geopolitical"
    assert classify_event("A completely unrelated sentence")[0] == "other"
