def safety_score(spd, spd_limit, follow_dist):
    score = 100
    score -= (spd - spd_limit)**2
    if follow_dist < optimal_follow(spd):
        score -= ((optimal_follow(spd) - follow_dist)/2)**2
    return max(score, 0)

def optimal_follow(spd):
    return spd * 1.5