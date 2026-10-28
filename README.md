# Boy Band x In Real Life: From 30 Contestants to 5

A data project on ABC's 2017 competition *Boy Band* and the group it produced, **In Real Life (IRL)**: who survived each week, what the winners had in common (and didn't), and what happened to the band after the finale.

Built from public sources (Wikipedia, the In Real Life Fandom wiki, recaps and press). Every table carries confidence notes and a source-conflict log, so gaps are visible rather than papered over.

## Questions

1. How did the field shrink from 30 to 5, and where was the biggest cull?
2. Did age separate the winners from everyone else?
3. How rarely did the eventual winners land in the bottom?
4. Which contestants were grouped together most, and did the final five share a stage more than chance?
5. What did IRL's post-show run look like in time (releases, tours, split)?

## Findings

![Survival curve](charts/01_survival_curve.png)

**The field.** Night one cut 12 of 30; after that the show removed one or two boys a week (two each in Eps 6 and 7) until the finale named five.

![Ratings](charts/02_ratings.png)

**Ratings.** Viewership fell from 2.995M at the premiere to 2.134M in Ep 9 (about 29%), then ticked up to 2.399M for the finale.

![Age by outcome](charts/03_age_by_outcome.png)

**Age did not pick the winners.** Median age was 18 for the final five, 17 for the 13 eliminated top-18 boys, and 18.5 for the 12 cut on night one. With 30 people, treat this as description, not a model.

![Path to IRL](charts/04_path_to_irl.png)

![Bottom placements](charts/05_bottom_placements.png)

**Safe all the way.** Only one of the five, Sergio Calderon Jr., has a documented bottom placement (Ep 8, saved by viewers). Devin Hayes was the most-exposed contestant, in the bottom twice (saved in Ep 7, eliminated in Ep 8) alongside Andrew Bloom.

![Co-performance](charts/06_who_sang_with_whom.png)

**Who sang with whom.** The final five shared a group 1.7 times per pair on average, versus 1.1 for a finalist paired with an eliminated top-18 boy. Caution: the five simply lasted longer, so they had more chances to be grouped. This is survivorship, not evidence of chemistry.

![Timeline](charts/07_irl_timeline.png)

**The run.** Finale and debut single *Eyes Closed* (Aug 2017), two TV-heavy months, *Tattoo (How 'Bout You)* (early 2018, Mainstream Top 40 peak 29), two headline tours, the debut album *She Do* (Aug 23, 2019), then a split announced Jan 20, 2020, about 29 months after the finale.

## Data

| File | Contents |
|---|---|
| `data/boy_band_in_real_life_dataset.xlsx` | All tables in one workbook, with a live-formula Summary tab |
| `data/contestants.csv` | 30 contestants: age, hometown, status, elimination episode, bottoms |
| `data/episodes.csv` | 10 episodes with air dates, viewers, contestants remaining |
| `data/group_performances.csv` | 18 group performances with members and songs |
| `data/contestant_episode_progress.csv` | 141 contestant-by-episode rows |
| `data/final_five.csv`, `irl_discography.csv`, `irl_timeline.csv`, `irl_tours.csv`, `tv_appearances.csv`, `post_show_careers.csv` | The IRL side |
| `data/source_conflicts.csv` | Where sources disagreed and how I resolved it |

## Limitations (read before citing)

- Episode 9 solo songs and viewer-vote details were not in reachable sources.
- Episode 5 and 6 bottom placements are incomplete, so `bottom_appearances` undercounts.
- Several singles have only a year or month for release date.
- Ages and two hometowns differ across sources; both versions are kept.
- Group-song matches for a few groups are inferred by elimination and flagged in `song_confidence`.
- Original-artist labels are from general knowledge, not the fetched pages.
- n = 30, so all comparisons are descriptive. Group counts and co-performance are biased by survival.

## Reproduce

```bash
pip install pandas numpy matplotlib openpyxl
python analysis/build_charts.py
```

The script reads `data/*.csv` and writes `charts/*.png`.

## Possible extensions

- Add Spotify/streaming data for the discography once reachable.
- Fill the Ep 5 and 6 bottoms and Ep 9 songs from episode recaps to complete the elimination model.
- Compare against other TV-built groups (for example, Making the Band acts) for a bigger sample.
