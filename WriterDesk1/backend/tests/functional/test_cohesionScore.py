from app.cohesionCheck import generateExplanation

'''
    The following tests concern the function generateExplanation.
    This function combines the functions getTTRScore and getConnectiveScore
    such that a final score can be achieved. Next to that, 
    it gives explanations for the scores. 
'''
# Output: cohesionScore, feedback

# Possible test cases: 
# TTRScore >= 9
# TTRScore >= 7
# TTRScore >= 5
# TTRScore < 5
# connectivesScore >= 9
# connectivesScore >= 7
    # indexScore < 0.9
    # indexScore >= 0.9
# connectivesScore >= 5
    # indexScore < 0.9
    # indexScore >= 0.9
# connectivesScore < 5

# Could combine 2 test cases in one thing
# So TTRScore >= 9 and connectivesScore >= 9
# Then we get possible test cases as follows: 
# TTRScore >= 9 and connectivesScore >= 9
# TTRScore >= 7 and connectivesScore >= 7, indexScore < 0.9
# TTRScore >= 7 and connectivesScore >= 7, indexScore >= 0.9
# TTRScore >= 5 and connectivesScore >= 5, indexScore < 0.9
# TTRScore >= 5 and connectivesScore >= 5, indexScore >= 0.9
# TTRScore < 5 and connectivesScore < 5
# and then could have combo's 
# like TTRScore >=9 and connectivesScore < 5
