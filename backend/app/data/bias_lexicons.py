"""
Lexicons for bias detection.

This module contains word lists and phrases associated with different
political leanings and sensationalist language.
"""

# Words and phrases associated with left-leaning political content
LEFT_LEANING_TERMS = {
    # Progressive/Liberal terminology
    "progressive": 0.5,
    "liberal": 0.5,
    "social justice": 0.6,
    "universal healthcare": 0.7,
    "wealth inequality": 0.6,
    "income inequality": 0.6,
    "climate crisis": 0.6,
    "reproductive rights": 0.7,
    "pro-choice": 0.7,
    "gun control": 0.7,
    "systemic racism": 0.8,
    "defund the police": 0.9,
    "green new deal": 0.8,
    "transgender rights": 0.7,
    "democratic socialism": 0.8,
    "living wage": 0.6,
    "workers' rights": 0.6,
    "union rights": 0.6,
    "marginalized communities": 0.7,
    "equity": 0.6,
    
    # Left-leaning figures
    "alexandria ocasio-cortez": 0.7,
    "bernie sanders": 0.7,
    "elizabeth warren": 0.6,
    "ilhan omar": 0.7,
}

# Words and phrases associated with right-leaning political content
RIGHT_LEANING_TERMS = {
    # Conservative terminology
    "conservative": 0.5,
    "traditional values": 0.6,
    "free market": 0.6,
    "small government": 0.7,
    "lower taxes": 0.6,
    "tax cuts": 0.6,
    "deregulation": 0.7,
    "pro-life": 0.7,
    "second amendment": 0.7,
    "gun rights": 0.7,
    "individual liberty": 0.6,
    "religious freedom": 0.6,
    "family values": 0.6,
    "border security": 0.7,
    "law and order": 0.6,
    "tough on crime": 0.6,
    "national security": 0.5,
    "private healthcare": 0.6,
    "patriotism": 0.5,
    "illegal immigration": 0.7,
    
    # Right-leaning figures
    "donald trump": 0.6,
    "ron desantis": 0.7,
    "ted cruz": 0.7,
}

# Words and phrases associated with sensationalist language
SENSATIONALIST_TERMS = {
    # Extreme descriptors
    "outrageous": 0.7,
    "shocking": 0.7,
    "bombshell": 0.8,
    "explosive": 0.8,
    "horrific": 0.7,
    "devastating": 0.7,
    "destruction": 0.6,
    "catastrophic": 0.7,
    "crisis": 0.5,
    "scandal": 0.7,
    "slams": 0.6,
    "blasts": 0.6,
    "destroys": 0.8,
    "erupts": 0.6,
    "meltdown": 0.7,
    "chaos": 0.6,
    "mayhem": 0.7,
    "nightmare": 0.7,
    "disaster": 0.6,
    "emergency": 0.5,
    
    # Absolutist language
    "absolutely": 0.5,
    "completely": 0.5,
    "totally": 0.5,
    "utterly": 0.6,
    "never": 0.4,
    "always": 0.4,
    "every": 0.4,
    "all": 0.3,
    
    # Hyperbolic expressions
    "worst ever": 0.8,
    "best ever": 0.7,
    "greatest": 0.5,
    "perfect": 0.5,
    "incredible": 0.5,
    "unbelievable": 0.6,
    "massive": 0.5,
    "huge": 0.4,
    "enormous": 0.5,
    "terrifying": 0.7,
    "jaw-dropping": 0.8,
    "mind-blowing": 0.7,
    
    # Clickbait phrases
    "you won't believe": 0.9,
    "what happens next": 0.8,
    "will shock you": 0.9,
    "breaking news": 0.5,
    "this changes everything": 0.8,
}

# Neutral political terminology
NEUTRAL_POLITICAL_TERMS = {
    "policy": 0.0,
    "legislation": 0.0,
    "government": 0.0,
    "congress": 0.0,
    "senate": 0.0,
    "representative": 0.0,
    "politician": 0.0,
    "election": 0.0,
    "vote": 0.0,
    "ballot": 0.0,
    "democracy": 0.0,
    "republic": 0.0,
    "constitution": 0.0,
    "law": 0.0,
    "regulation": 0.0,
}