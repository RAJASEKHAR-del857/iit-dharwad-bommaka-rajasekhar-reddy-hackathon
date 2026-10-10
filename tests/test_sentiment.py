from sentinelrisk.nlp.sentiment import analyze_sentiment

def test_sentiment_ranges_and_labels():
    for text in ["Strong profit growth beats expectations", "Fraud losses and bankruptcy risk", "The company held a meeting"]:
        result = analyze_sentiment(text, use_finbert=False)
        assert result["label"] in {"positive", "negative", "neutral"}
        assert -1 <= result["score"] <= 1
        assert 0 <= result["confidence"] <= 1

def test_positive_and_negative_direction():
    assert analyze_sentiment("profits grew and strong growth", False)["score"] > 0
    assert analyze_sentiment("fraud losses and bankruptcy", False)["score"] < 0
