# March Madness Selection

Uses Nate Silver's prediction model to weight teams' chances, then "rolls a dice" to see who wins. One simulation that was [unbiased](./unbiased.txt) past using the model, and another that was [slightly biased to produce upsets](./upset_biased.txt).

The algo to decide is pretty simple. Nate Silver's rankings are presented in the format of each team's chances to advance to that certain round. So for each match, we calculate a `to_beat` based on the difference of those numbers, then have the lower team "roll" to see if they can beat that number:

```python
to_beat = higher_rated_team - (lower_rated_team / 2)
roll = random.uniform(higer_rated_team)
if upset_biased:
    roll *= 1.25
if lower_rated_team_roll >= to_beat:
    # Upset
else:
    # Fate as we expected
```
